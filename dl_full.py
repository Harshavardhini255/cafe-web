import requests, re, json, os

posts = [
    ('mini-blueberry-bliss.jpg', 'https://www.instagram.com/p/DYM-jYNE8SV/'),
    ('golden-crunch-burger.jpg', 'https://www.instagram.com/p/DX4WHBXE3_3/'),
    ('classic-affogato.jpg', 'https://www.instagram.com/p/DXviAj_kwgL/'),
    ('cold-kaapi-scoop.jpg', 'https://www.instagram.com/p/DXt-HdME_zd/'),
    ('herbed-rice-chicken.jpg', 'https://www.instagram.com/p/DXrfKvxk49E/'),
    ('potato-chicken-skewers.jpg', 'https://www.instagram.com/p/DXgTXPAk_Mq/'),
    ('chicken-marinara.jpg', 'https://www.instagram.com/p/DXUHTKzkwEV/'),
    ('classic-tiramisu.jpg', 'https://www.instagram.com/p/DXRncsGE3kM/'),
    ('pistachio-tiramisu.jpg', 'https://www.instagram.com/p/DXQjscoE8Bx/'),
    ('choco-hazelnut-tiramisu.jpg', 'https://www.instagram.com/p/DXOQd1-DXub/'),
    ('caramel-crunch.jpg', 'https://www.instagram.com/p/DYzPQJGk4-o/'),
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
static_dir = r'C:\Users\Dell\flow-kbeauty\static'

for name, url in posts:
    path = os.path.join(static_dir, name)
    try:
        r = requests.get(url, headers=headers, timeout=15)
        # Try to find the full-size image in the JSON embedded data
        # Look for display_url or display_src in the page source
        matches = re.findall(r'"display_url":"([^"]+)"', r.text)
        if not matches:
            matches = re.findall(r'"display_src":"([^"]+)"', r.text)
        if not matches:
            matches = re.findall(r'<img[^>]+src="([^"]+)"[^>]*style="[^"]*object-fit:cover', r.text)
        if matches:
            img_url = matches[0].replace('\\u0026', '&')
            print(f'FULL {name}')
            img_r = requests.get(img_url, headers=headers, timeout=30)
            with open(path, 'wb') as f:
                f.write(img_r.content)
            from PIL import Image
            img_check = Image.open(path)
            print(f'  OK {len(img_r.content)} bytes - {img_check.size[0]}x{img_check.size[1]}')
        else:
            # Fallback: try the og:image
            m = re.search(r'<meta property="og:image"[^>]+content="([^"]+)"', r.text)
            if m:
                img_url = m.group(1).replace('&amp;', '&')
                print(f'OG {name}')
                img_r = requests.get(img_url, headers=headers, timeout=30)
                with open(path, 'wb') as f:
                    f.write(img_r.content)
                from PIL import Image
                img_check = Image.open(path)
                print(f'  {len(img_r.content)} bytes - {img_check.size[0]}x{img_check.size[1]}')
            else:
                print(f'NO IMAGE {name}')
    except Exception as e:
        print(f'ERR {name}: {e}')
