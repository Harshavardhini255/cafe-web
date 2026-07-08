import urllib.request, re, json, os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
url = 'https://www.instagram.com/s/aGlnaGhpZ2h0OjE4MTAyOTM0NDgzOTk1MjQ2?story_media_id=3896663315666149452_39801590188'
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=20) as r:
    html = r.read().decode('utf-8', errors='replace')

# Search for various JSON patterns
patterns = [
    r'window\.__INITIAL_STATE__\s*=\s*({.*?});',
    r'"display_url":"([^"]+)"',
    r'"display_src":"([^"]+)"',
    r'\"image_versions2\"[^}]+}',
    r'"src":"([^"]+)"',
]
for p in patterns:
    m = re.search(p, html, re.DOTALL)
    if m:
        print(f'Found pattern: {p[:40]}')
        print(m.group(0)[:200])
        print('---')
