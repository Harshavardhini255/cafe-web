import requests, re
from PIL import Image
from io import BytesIO

headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get('https://www.instagram.com/p/DXt-HdME_zd/', headers=headers, timeout=15)
m = re.search(r'<meta property="og:image"[^>]+content="([^"]+)"', r.text)
if m:
    url = m.group(1).replace('&amp;', '&')
    print('og:image:', url[:120])
    hr = requests.get(url, headers=headers, timeout=15)
    img = Image.open(BytesIO(hr.content))
    print(f'Size: {img.size[0]}x{img.size[1]}')

# Also check the other posts
urls = [
    'https://www.instagram.com/p/DYM-jYNE8SV/',
    'https://www.instagram.com/p/DX4WHBXE3_3/',
    'https://www.instagram.com/p/DXrfKvxk49E/',
]
for u in urls:
    r = requests.get(u, headers=headers, timeout=15)
    m = re.search(r'<meta property="og:image"[^>]+content="([^"]+)"', r.text)
    if m:
        url2 = m.group(1).replace('&amp;', '&')
        hr = requests.get(url2, headers=headers, timeout=15)
        img = Image.open(BytesIO(hr.content))
        # Extract crop param
        crop = re.search(r'c(\d+)\.(\d+)\.(\d+)\.(\d+)', url2)
        if crop:
            print(f'{u.split("/p/")[1].split("/")[0]}: {img.size[0]}x{img.size[1]} crop=({crop.group(1)},{crop.group(2)},{crop.group(3)},{crop.group(4)})')
        else:
            print(f'{u.split("/p/")[1].split("/")[0]}: {img.size[0]}x{img.size[1]} no crop')
