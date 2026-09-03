/* The Worker in front of the static assets.
 *
 * One job: POST /api/contact accepts the quote/demo form and delivers it by
 * email through MailerSend - the sender already in this domain's SPF record.
 * Everything else falls through to the static assets, so the site, the PDFs
 * and the 404 behave exactly as before.
 *
 * Without a MAILERSEND_TOKEN secret the endpoint answers {ok:false,
 * fallback:true} and the front end quietly reverts to the mailto link, so
 * deploying this before the secret exists breaks nothing.
 *
 *   npx wrangler secret put MAILERSEND_TOKEN
 */

const DEST = "app@rocketx.app";
const FROM = { email: "website@rocketx.app", name: "RocketX Website" };
const TOPICS = { quote: "Quote request", demo: "Demo request" };
const MAX = { name: 200, email: 254, company: 200, message: 5000 };

function bad(status, msg) {
  return new Response(JSON.stringify({ ok: false, error: msg }), {
    status,
    headers: { "content-type": "application/json" },
  });
}

function clean(v, max) {
  return String(v == null ? "" : v).replace(/[\r\n\t]+/g, " ").trim().slice(0, max);
}

async function handleContact(request, env) {
  let data;
  try {
    data = await request.json();
  } catch (e) {
    return bad(400, "invalid json");
  }

  // the honeypot field is visually hidden; anything in it is a bot
  if (clean(data.website, 50) !== "") {
    return new Response(JSON.stringify({ ok: true }), {
      headers: { "content-type": "application/json" },
    });
  }

  const name = clean(data.name, MAX.name);
  const email = clean(data.email, MAX.email);
  const company = clean(data.company, MAX.company);
  const topic = TOPICS[data.topic] ? data.topic : "quote";
  const lang = /^[a-z]{2}$/.test(String(data.lang)) ? data.lang : "en";
  const message = String(data.message == null ? "" : data.message)
    .trim()
    .slice(0, MAX.message);

  if (name.length < 2) return bad(422, "name");
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) return bad(422, "email");

  if (!env.MAILERSEND_TOKEN) {
    return new Response(JSON.stringify({ ok: false, fallback: true }), {
      headers: { "content-type": "application/json" },
    });
  }

  const subject =
    "RocketX — " + TOPICS[topic] + " — " + (company || name) +
    " [" + lang + "]";
  const text =
    TOPICS[topic] + " from the website (" + lang + ")\n\n" +
    "Name:    " + name + "\n" +
    "Email:   " + email + "\n" +
    "Company: " + (company || "-") + "\n\n" +
    (message ? message + "\n" : "(no message)\n");

  const res = await fetch("https://api.mailersend.com/v1/email", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      authorization: "Bearer " + env.MAILERSEND_TOKEN,
    },
    body: JSON.stringify({
      from: FROM,
      to: [{ email: DEST }],
      reply_to: { email: email, name: name },
      subject: subject,
      text: text,
    }),
  });

  if (res.status === 202 || res.status === 200) {
    return new Response(JSON.stringify({ ok: true }), {
      headers: { "content-type": "application/json" },
    });
  }
  // delivery refused (bad token, unverified domain, rate limit): let the
  // front end fall back to mailto rather than swallowing the lead
  return new Response(JSON.stringify({ ok: false, fallback: true }), {
    headers: { "content-type": "application/json" },
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/contact") {
      if (request.method === "POST") return handleContact(request, env);
      return bad(405, "method");
    }
    // Short links for print. A QR code on a mailed letter cannot be edited
    // once it is in the post, so the PRINTED path stays fixed here and the
    // file it resolves to stays movable. 302 and not 301 for the same
    // reason: a permanent redirect is cached hard by browsers and is
    // effectively unrecallable, which is the wrong property for a link with
    // a six-year life printed on paper.
    // NOTE: "/1page" itself is deliberately absent. It is a real page now
    // (1page/index.html), served by ASSETS below - the letter's QR lands on
    // something with tap targets instead of a PDF in a phone viewer. The
    // language variants below still go straight to their PDFs.
    const SHORT = {
      "/1page/de": "/assets/rocketx-one-page-de.pdf",
      "/1page/es": "/assets/rocketx-one-page-es.pdf",
      "/1page/nl": "/assets/rocketx-one-page-nl.pdf",
      "/1page/fr": "/assets/rocketx-one-page-fr.pdf",
    };
    const short = SHORT[url.pathname.replace(/\/+$/, "") || "/"];
    if (short) {
      return Response.redirect(new URL(short, url).toString(), 302);
    }

    return env.ASSETS.fetch(request);
  },
};
