import requests, re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
url = 'https://www.instagram.com/p/DXt-HdME_zd/'
r = requests.get(url, headers=headers, timeout=15)
# Find all image URLs
urls = re.findall(r'https?://[^"\'\\\s]+\.(?:jpg|png|webp)[^"\'\\\s]*', r.text)
seen = set()
for u in urls:
    if u not in seen:
        seen.add(u)
        print(u[:150])
