import urllib.request, re, os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

static = r'C:\Users\Dell\flow-kbeauty\static'

# For each story media_id, try to get the image via the full story URL
media_ids = [
    ('cake-1', '3896663315666149452_39801590188'),
    ('cake-2', '3901849117463353144_39801590188'),
    ('cake-3', '3901853254539910999_39801590188'),
    ('cake-4', '3920245939500202166_39801590188'),
    ('cake-5', '3923034560884050370_39801590188'),
    ('cake-6', '3930953824756511614_39801590188'),
    ('cake-7', '3936167574865994948_39801590188'),
    ('cake-8', '3936168276191830974_39801590188'),
    ('cake-9', '3936169987434286630_39801590188'),
]

for name, mid in media_ids:
    url = f'https://www.instagram.com/s/aGlnaGhpZ2h0OjE4MTAyOTM0NDgzOTk1MjQ2?story_media_id={mid}'
    try:
        req = urllib.request.Request(url, headers=headers)
        req.add_header('Cookie', 'ig_did=FAKE; csrftoken=fake')
        with urllib.request.urlopen(req, timeout=20) as r:
            html = r.read().decode('utf-8', errors='replace')
        # Try to find any scontent.cdninstagram.com URL
        for m in re.finditer(r'https://scontent\.cdninstagram\.com[^"\' <>]+\.(?:jpg|png|webp)', html):
            img_url = m.group()
            # Clean URL - remove escaped chars
            img_url = img_url.replace('\\', '')
            print(f'{name}: {img_url[:100]}...')
            # Download
            req2 = urllib.request.Request(img_url, headers=headers)
            with urllib.request.urlopen(req2, timeout=15) as r2:
                data = r2.read()
            if len(data) > 5000:
                path = os.path.join(static, f'{name}.jpg')
                with open(path, 'wb') as f:
                    f.write(data)
                print(f'  -> Saved ({len(data)//1024}KB)')
            break
        else:
            print(f'{name}: no image URL found in page')
    except Exception as e:
        print(f'{name}: {str(e)[:60]}')
