import urllib.request, re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
url = 'https://www.instagram.com/s/aGlnaGhpZ2h0OjE4MTAyOTM0NDgzOTk1MjQ2?story_media_id=3896663315666149452_39801590188'
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=20) as r:
    html = r.read().decode('utf-8', errors='replace')

# Find all script tags with JSON
for m in re.finditer(r'<script[^>]*type="application/json"[^>]*>(.*?)</script>', html, re.DOTALL):
    text = m.group(1)
    if 'image' in text.lower():
        print(text[:500])
        print('---')

# Also search for any jpg/png URLs
for m in re.finditer(r'https?://[^"\' <>\']+\.(?:jpg|png|webp)[^"\' <>\']*', html):
    print(m.group()[:150])
