import urllib.request, re, os, sys

def fetch_og(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            html = r.read().decode('utf-8', errors='replace')
        m = re.search(r'og:image[^>]+content="([^"]+)"', html)
        if m:
            return m.group(1)
        # try to find any cdn instagram image
        m2 = re.search(r'https://scontent\.cdninstagram\.com[^"\'\\<> ]+', html)
        if m2:
            return m2.group()
        return None
    except Exception as e:
        return f'Error: {e}'

static = r'C:\Users\Dell\flow-kbeauty\static'

cakes = [
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

base = 'https://www.instagram.com/s/aGlnaGhpZ2h0OjE4MTAyOTM0NDgzOTk1MjQ2?story_media_id={}'

for name, media_id in cakes:
    url = base.format(media_id)
    og_url = fetch_og(url)
    if og_url and og_url.startswith('http'):
        print(f'{name}: {og_url[:80]}...')
        path = os.path.join(static, f'{name}.jpg')
        req2 = urllib.request.Request(og_url, headers=headers)
        try:
            with urllib.request.urlopen(req2, timeout=20) as r:
                with open(path, 'wb') as f:
                    f.write(r.read())
            print(f'  -> Saved ({os.path.getsize(path)//1024}KB)')
        except Exception as e:
            print(f'  -> DL Error: {e}')
    else:
        print(f'{name}: No image ({og_url})')
