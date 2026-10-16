#!/usr/bin/env python3
"""Baut die QR-Speisekarte.

    python3 assets-src/build.py            → index.html (für den Webserver, Dateien unter assets/)
    python3 assets-src/build.py --inline   → Vorschau_Speisekarte.html (eine einzige Datei, alles eingebettet)
"""
import base64
import glob
import json
import os
import re
import subprocess
import sys
import urllib.parse
from html import escape as html_escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import menu_data as md  # noqa: E402

INLINE = "--inline" in sys.argv
MIME = {".webm": "video/webm", ".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg", ".mp4": "video/mp4", ".woff2": "font/woff2"}

PATTERN_SVG = ("<svg xmlns='http://www.w3.org/2000/svg' width='120' height='120' viewBox='0 0 120 120'>"
               "<g fill='none' stroke='#d9b46a' stroke-width='1.5'>"
               "<path d='M60 18 L72 48 L102 60 L72 72 L60 102 L48 72 L18 60 L48 48 Z'/>"
               "<path d='M30 30 L90 30 L90 90 L30 90 Z' transform='rotate(45 60 60)'/>"
               "<circle cx='60' cy='60' r='9'/><circle cx='0' cy='0' r='5'/><circle cx='120' cy='0' r='5'/>"
               "<circle cx='0' cy='120' r='5'/><circle cx='120' cy='120' r='5'/></g></svg>")


def data_uri(rel):
    path = os.path.join(ROOT, "assets", rel)
    ext = os.path.splitext(path)[1]
    return f"data:{MIME[ext]};base64," + base64.b64encode(open(path, "rb").read()).decode()


def ref(rel):
    return data_uri(rel) if INLINE else "assets/" + rel


FONT_LAT = ("U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308,\n"
            "          U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD")
FONT_EXT = ("U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329,\n"
            "          U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF")


def font_faces():
    """Fraunces (Überschriften) und Montserrat (Preise), lokal, je Latein + Latein-Erweitert (Türkisch)."""
    out = []
    for fam, file in [("Fraunces", "fraunces-normal"), ("Montserrat", "montserrat")]:
        for sub, rng in (("latin", FONT_LAT), ("latin-ext", FONT_EXT)):
            out.append(f'''      @font-face {{
        font-family: "{fam}";
        font-style: normal;
        font-weight: 100 900;
        font-display: swap;
        src: url(assets/fonts/{file}-{sub}.woff2) format("woff2");
        unicode-range: {rng};
      }}''')
    return "\n".join(out)


fonts = font_faces()
# Kursiv nur für den Slogan: statt 270 KB eine Mini-Schrift mit genau diesen Buchstaben
fonts += """
      @font-face {
        font-family: "Fraunces";
        font-style: italic;
        font-weight: 100 900;
        font-display: swap;
        src: url(assets/fonts/fraunces-italic-slogan.woff2) format("woff2");
      }"""
PRELOAD = "\n".join(f'    <link rel="preload" href="assets/fonts/{f}.woff2" as="font" type="font/woff2" crossorigin />'
                    for f in ("fraunces-normal-latin", "montserrat-latin"))
if INLINE:
    for f in glob.glob(os.path.join(ROOT, "assets", "fonts", "*.woff2")):
        rel = "fonts/" + os.path.basename(f)
        fonts = fonts.replace(f"url(assets/{rel})", f"url({data_uri(rel)})")

# ---- Karte vorab in HTML schreiben (Node führt denselben Code aus wie der Browser)
CORE = os.path.join(HERE, "render_core.js")
data_json = json.dumps(md.DATA, ensure_ascii=False)
tmp = os.path.join(HERE, ".data.json")
open(tmp, "w", encoding="utf-8").write(data_json)
NODE = r"""
const fs = require("fs"), path = require("path");
const [coreFile, dataFile, assetsDir, mode] = process.argv.slice(1);
const HYE_CORE = require(coreFile);
const DATA = JSON.parse(fs.readFileSync(dataFile, "utf8"));
const used = new Set();
const MIME = { ".webp": "image/webp", ".jpg": "image/jpeg", ".png": "image/png" };
const A = (p) => {
  if (mode !== "inline") return "assets/" + p;
  used.add(p);
  return "data:" + MIME[path.extname(p)] + ";base64," + fs.readFileSync(path.join(assetsDir, p)).toString("base64");
};
const R = HYE_CORE(DATA, { A }).renderAll("de", "mit");
R.used = [...used];
process.stdout.write(JSON.stringify(R));
"""
res = subprocess.run(["node", "-e", NODE, CORE, tmp, os.path.join(ROOT, "assets"), "inline" if INLINE else "web"],
                     capture_output=True, text=True, check=True)
os.remove(tmp)
R = json.loads(res.stdout)

assets = {}
if INLINE:
    used = set(R["used"])
    for f in sorted(glob.glob(os.path.join(ROOT, "assets", "img", "*.webp")) +
                    glob.glob(os.path.join(ROOT, "assets", "video", "*.mp4"))):
        rel = os.path.relpath(f, os.path.join(ROOT, "assets"))
        if rel in used or rel.startswith("video/hero"):
            continue  # steht schon in der Seite bzw. Hero direkt im HTML
        assets[rel] = data_uri(rel)

html = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
repl = {
    "/*__FONTS__*/": fonts,
    "/*__CORE__*/": open(CORE, encoding="utf-8").read(),
    "__PATTERN__": "data:image/svg+xml," + urllib.parse.quote(PATTERN_SVG),
    "__ICON48__": ref("brand/icon-48.png"),
    "__ICON180__": ref("brand/icon-180.png"),
    "__LOGO_WEBP__": ref("brand/logo-gold.webp"),
    "__HERO_VIDEO__": ref("video/hero.mp4"),
    "__HERO_WEBM__": "" if INLINE else "assets/video/hero.webm",
    "__HERO_POSTER__": ref("video/hero.jpg"),
    "__FONT_PRELOAD__": "" if INLINE else PRELOAD,
    "__ASSETS__": json.dumps(assets) if INLINE else "null",
    "__DATA__": json.dumps(md.DATA, ensure_ascii=False, separators=(",", ":")),
    "__TITLE__": html_escape(R["title"]),
    "__PRE_MAIN__": R["main"],
    "__PRE_CHIPS__": R["chips"],
    "__PRE_LM__": R["lm"],
    "__PRE_LANG__": R["langSwitch"],
    "__PRE_LEGEND__": R["legend"],
}
for k, v in R["ui"].items():
    repl[f"__UI_{k}__"] = html_escape(v)
for k, v in repl.items():
    if k not in html:
        continue
    html = html.replace(k, v)
left = sorted(set(re.findall(r"__(?:PRE|UI)_[A-Za-z_]+__|__[A-Z0-9_]{4,}__", html)))
assert not left, left
out = os.path.join(ROOT, "Vorschau_Speisekarte.html" if INLINE else "index.html")
open(out, "w", encoding="utf-8").write(html)
print(os.path.basename(out), f"{os.path.getsize(out) / 1048576:.2f} MB")
