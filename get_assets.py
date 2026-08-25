#!/usr/bin/env python3
"""Download RocketX site assets from the Framer CDN into ./assets/.
Run this once, from the folder containing index.html:  python3 get_assets.py
"""
import os, urllib.request

ASSETS = {
 "assets/logo.png":     "https://framerusercontent.com/images/wg0B1DP6WhoAmvL3py7z1zuGaiA.png?width=500&height=500",
 "assets/product-1.webp":"https://framerusercontent.com/images/7hEMnzNW8TKI35mykrwNnPK59m4.webp?width=900&height=900",
 "assets/product-2.webp":"https://framerusercontent.com/images/qygTke3Lz3OnuVTqaf6hwZMPqg.webp?width=700&height=700",
 "assets/product-3.webp":"https://framerusercontent.com/images/Kd1nzo6lP4rR3cKegRhIkIqD8w.webp?width=600&height=600",
 "assets/poster.webp":  "https://framerusercontent.com/images/V58LrdFh5mIXc0J15IsIcr2Uuo.webp?width=1600&height=1600",
 "assets/demo.mp4":     "https://framerusercontent.com/assets/XWnzN2LkYQkgWYrpoQWvJt3VA.mp4",
 "assets/photo-1.webp": "https://framerusercontent.com/images/K3p4vDOZMx9XlZYJBJzTGqsjIts.webp?width=1400",
 "assets/photo-2.webp": "https://framerusercontent.com/images/7rykZ1X19HC6ibxzXY7RVL6VQo.webp?width=1000",
}

os.makedirs("assets", exist_ok=True)
opener = urllib.request.build_opener()
opener.addheaders = [("User-Agent", "Mozilla/5.0")]
urllib.request.install_opener(opener)

ok = True
for path, url in ASSETS.items():
    try:
        print(f"  downloading {path} ...", end=" ", flush=True)
        urllib.request.urlretrieve(url, path)
        print(f"{os.path.getsize(path)//1024} KB")
    except Exception as e:
        ok = False
        print(f"FAILED ({e})")

print()
print("Done — open index.html in a browser." if ok
      else "Some downloads failed — check your connection and rerun.")
