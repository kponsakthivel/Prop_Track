"""Adds the iPhone-install (PWA) tags to index.html in the deploy folder.
Safe to run more than once. Your source www/index.html is never changed."""
import re, sys

path = sys.argv[1]
html = open(path, encoding="utf-8").read()

if "rel=\"manifest\"" in html or "rel='manifest'" in html:
    print("PWA tags already present; nothing to do.")
    sys.exit(0)

tags = """
<link rel="manifest" href="manifest.json">
<link rel="apple-touch-icon" href="icons/icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="PropTrack">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="#1e6fd9">
"""

# make sure the viewport covers the notch area
vp = re.search(r'<meta[^>]*name=["\']viewport["\'][^>]*>', html, re.I)
if vp:
    tag = vp.group(0)
    if "viewport-fit" not in tag:
        new = re.sub(r'content=(["\'])(.*?)\1', lambda m: f'content={m.group(1)}{m.group(2)}, viewport-fit=cover{m.group(1)}', tag, flags=re.I)
        html = html.replace(tag, new)
else:
    tags = '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">' + tags

script = """
<script>
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("sw.js").catch(function () {});
    });
  }
</script>
"""

if re.search(r"</head>", html, re.I):
    html = re.sub(r"</head>", tags + "</head>", html, count=1, flags=re.I)
else:
    html = tags + html
if re.search(r"</body>", html, re.I):
    html = re.sub(r"</body>", script + "</body>", html, count=1, flags=re.I)
else:
    html += script

open(path, "w", encoding="utf-8").write(html)
print("PWA tags added.")
