import requests, re
from PIL import Image
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
static_dir = r'C:\Users\Dell\flow-kbeauty\static'

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

for name, url in posts:
    path = os.path.join(static_dir, name)
    try:
        r = requests.get(url, headers=headers, timeout=15)
        all_urls = re.findall(r'https://scontent\.cdninstagram\.com[^"\'\\\s]+\.jpg[^"\'\\\s]*', r.text)
        # Find the one without crop params or with the largest size
        best_url = None
        for u in all_urls:
            if '_s640x640' in u or '_s1080x1080' in u:
                # Replace with full size
                full = re.sub(r'_s\d+x\d+', '_s1080x1080', u)
                full = re.sub(r'c\d+\.\d+\.\d+\.\d+a_', '', full)
                full = re.sub(r'stp=[^&]+&', '', full)
                best_url = full
                break
            if '640x640' not in u:
                best_url = u
                break
        if not best_url and all_urls:
            best_url = all_urls[0]
        
        if best_url:
            print(f'DL {name}')
            print(f'  URL: {best_url[:120]}')
            img_r = requests.get(best_url, headers=headers, timeout=30)
            if img_r.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(img_r.content)
                img = Image.open(path)
                print(f'  {len(img_r.content)} bytes - {img.size[0]}x{img.size[1]}')
            else:
                print(f'  FAILED HTTP {img_r.status_code}')
        else:
            print(f'NO URL {name}')
    except Exception as e:
        print(f'ERR {name}: {e}')
