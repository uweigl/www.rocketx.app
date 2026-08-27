# -*- coding: utf-8 -*-
"""Text extraction for Chrome-printed PDFs.

Chrome emits Type0 fonts with ToUnicode CMaps and Flate content streams, which
makes a small, honest extractor possible: decompress, walk each page's content
stream, decode every shown string through the font's own CMap. Returns text per
page, so a claim can be located, not just found.
"""
import io, re, zlib


def _objects(d):
    """obj number -> (dict-ish header bytes, raw stream bytes or None)

    Streams hold arbitrary bytes, so splitting on "endobj" mis-parses any file
    whose compressed data happens to contain it. Split on object headers
    instead; the stray-match risk is far smaller and detectable."""
    out = {}
    heads = list(re.finditer(rb"(?:^|[\r\n>])(\d+)\s+0\s+obj", d))
    for idx, m in enumerate(heads):
        num = int(m.group(1))
        end = heads[idx + 1].start() if idx + 1 < len(heads) else len(d)
        body = d[m.end():end]
        e = body.rfind(b"endobj")
        if e != -1:
            body = body[:e]
        sm = re.search(rb"stream\r?\n", body)
        if sm:
            head = body[:sm.start()]
            raw = body[sm.end():]
            em = raw.rfind(b"endstream")
            raw = raw[:em].rstrip(b"\r\n")
            out[num] = (head, raw)
        else:
            out[num] = (body, None)
    return out


def _inflate(head, raw):
    if raw is None:
        return None
    if b"FlateDecode" in head:
        try:
            return zlib.decompress(raw)
        except zlib.error:
            return None
    return raw


def _cmap(data):
    """ToUnicode stream -> {code:int -> unicode str}"""
    m = {}
    txt = data.decode("latin1")
    for bl in re.finditer(r"beginbfchar(.*?)endbfchar", txt, re.S):
        for src, dst in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", bl.group(1)):
            u = bytes.fromhex(dst).decode("utf-16-be", "ignore")
            m[int(src, 16)] = u
    for bl in re.finditer(r"beginbfrange(.*?)endbfrange", txt, re.S):
        body = bl.group(1)
        for a, b, c in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", body):
            lo, hi, base = int(a, 16), int(b, 16), int(c, 16)
            for i in range(hi - lo + 1):
                m[lo + i] = chr(base + i)
        for a, b, arr in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*\[(.*?)\]", body, re.S):
            lo = int(a, 16)
            dsts = re.findall(r"<([0-9A-Fa-f]+)>", arr)
            for i, dst in enumerate(dsts):
                m[lo + i] = bytes.fromhex(dst).decode("utf-16-be", "ignore")
    return m


def _ref(v):
    m = re.match(rb"\s*(\d+)\s+0\s+R", v)
    return int(m.group(1)) if m else None


def _unescape(b):
    out, i = [], 0
    while i < len(b):
        c = b[i]
        if c == 0x5C and i + 1 < len(b):
            n = b[i + 1]
            if n in b"nrtbf()\\":
                out.append({0x6E: 10, 0x72: 13, 0x74: 9, 0x62: 8, 0x66: 12}.get(n, n))
                i += 2
                continue
            m = re.match(rb"\\([0-7]{1,3})", b[i:])
            if m:
                out.append(int(m.group(1), 8) & 0xFF)
                i += len(m.group(0))
                continue
        out.append(c)
        i += 1
    return bytes(out)


def extract(path):
    d = io.open(path, "rb").read()
    objs = _objects(d)

    # font object -> (code map, bytes per code)
    # Chrome renders Google web fonts as Type3 with one-byte codes and keeps
    # locally installed faces as Type0/Identity-H with two-byte codes
    fontmaps = {}
    for num, (head, raw) in objs.items():
        if b"/Type" in head and b"/Font" in head and b"/Subtype" in head:
            st = re.search(rb"/Subtype\s*/(\w+)", head)
            width = 2 if st and st.group(1) == b"Type0" else 1
            tu = re.search(rb"/ToUnicode\s+(\d+)\s+0\s+R", head)
            cmap = {}
            if tu and tu_int(tu) in objs:
                h2, r2 = objs[tu_int(tu)]
                data = _inflate(h2, r2)
                if data:
                    cmap = _cmap(data)
            fontmaps[num] = (cmap, width)
    # some Chrome builds put ToUnicode on the descendant; also accept any
    # object that IS a CMap and link it to the font that references it
    pages = []
    for num, (head, raw) in objs.items():
        if re.search(rb"/Type\s*/Page[^s]", head):
            pages.append((num, head))
    pages.sort()

    out = []
    for num, head in pages:
        # font name -> font object for this page
        res = {}
        fm = re.search(rb"/Font\s*<<(.*?)>>", head, re.S)
        if not fm:
            rm = re.search(rb"/Resources\s+(\d+)\s+0\s+R", head)
            if rm and int(rm.group(1)) in objs:
                fm = re.search(rb"/Font\s*<<(.*?)>>", objs[int(rm.group(1))][0], re.S)
        if fm:
            for name, ref in re.findall(rb"/(\w+)\s+(\d+)\s+0\s+R", fm.group(1)):
                res[name.decode()] = int(ref)
        cm = re.search(rb"/Contents\s+(\d+)\s+0\s+R", head)
        text = []
        if cm and int(cm.group(1)) in objs:
            h2, r2 = objs[int(cm.group(1))]
            data = _inflate(h2, r2)
            if data:
                cur = None
                toks = re.finditer(
                    rb"/(\w+)\s+[\d.]+\s+Tf|\(((?:[^()\\]|\\.)*)\)\s*Tj|<([0-9A-Fa-f\s]+)>\s*Tj|\[(.*?)\]\s*TJ|T\*|Td|TD",
                    data, re.S)
                for t in toks:
                    if t.group(1):
                        cur = fontmaps.get(res.get(t.group(1).decode()), ({}, 1))
                        continue
                    if cur is None:
                        cur = ({}, 1)
                    frags = []
                    if t.group(2) is not None:
                        frags = [_unescape(t.group(2))]
                    elif t.group(3) is not None:
                        frags = [bytes.fromhex(t.group(3).decode().replace("\n", "").replace(" ", ""))]
                    elif t.group(4) is not None:
                        for pm in re.finditer(rb"\(((?:[^()\\]|\\.)*)\)|<([0-9A-Fa-f\s]+)>", t.group(4), re.S):
                            if pm.group(1) is not None:
                                frags.append(_unescape(pm.group(1)))
                            else:
                                frags.append(bytes.fromhex(pm.group(2).decode().replace("\n", "").replace(" ", "")))
                    else:
                        continue
                    cmap, width = cur
                    for fb in frags:
                        s = ""
                        if width == 2:
                            for i in range(0, len(fb) - 1, 2):
                                s += cmap.get((fb[i] << 8) | fb[i + 1], "")
                        else:
                            for c in fb:
                                s += cmap.get(c, "")
                        text.append(s)
        out.append("".join(text))
    return out


def tu_int(m):
    return int(m.group(1))


if __name__ == "__main__":
    import sys
    pages = extract(sys.argv[1])
    for i, p in enumerate(pages):
        print("--- page %d (%d chars)" % (i + 1, len(p)))
        print(p[:400].encode("utf-8", "replace").decode("utf-8"))
