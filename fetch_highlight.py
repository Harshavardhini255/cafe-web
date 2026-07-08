import urllib.request, re, base64, os

# Decode the highlight ID
s = 'aGlnaGhpZ2h0OjE4MTAyOTM0NDgzOTk1MjQ2'
decoded = base64.b64decode(s).decode()
highlight_id = decoded.split(':')[1]
print(f'Highlight ID: {highlight_id}')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Try to fetch the highlight page
url = f'https://www.instagram.com/stories/highlights/{highlight_id}/'
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=20) as r:
    html = r.read().decode('utf-8', errors='replace')

# Look for og:image
m = re.search(r'og:image[^>]+content="([^"]+)"', html)
if m:
    print(f'OG Image: {m.group(1)[:120]}')
else:
    print('No og:image found')

# Search for any jpg/png in scontent
for m2 in re.finditer(r'https://scontent\.cdninstagram\.com[^"\' <>]+\.(?:jpg|png)', html):
    print(f'Found: {m2.group()[:120]}')

# Try /media endpoint for each story_media_id
static = r'C:\Users\Dell\flow-kbeauty\static'
media_ids = [
    ('aarthi-cake', '3896663315666149452_39801590188'),
    ('kanaga-cake', '3901849117463353144_39801590188'),
    ('jerona-cake', '3901853254539910999_39801590188'),
    ('cake-4', '3920245939500202166_39801590188'),
    ('cake-5', '3923034560884050370_39801590188'),
    ('cake-6', '3930953824756511614_39801590188'),
    ('cake-7', '3936167574865994948_39801590188'),
    ('cake-8', '3936168276191830974_39801590188'),
    ('cake-9', '3936169987434286630_39801590188'),
]

for name, media_id in media_ids:
    # Try using the full media_id as a post shortcode
    for endpoint in [f'https://www.instagram.com/p/{media_id}/media/',
                     f'https://www.instagram.com/p/{media_id.split("_")[0]}/media/']:
        try:
            req2 = urllib.request.Request(endpoint + '?size=l', headers=headers)
            with urllib.request.urlopen(req2, timeout=10) as r2:
                data = r2.read()
                path = os.path.join(static, f'{name}.jpg')
                with open(path, 'wb') as f:
                    f.write(data)
                print(f'{name}: OK ({len(data)//1024}KB) from {endpoint[:60]}...')
                break
        except Exception as e:
            pass
    else:
        print(f'{name}: FAILED all endpoints')
