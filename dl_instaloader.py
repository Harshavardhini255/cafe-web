import instaloader, os

L = instaloader.Instaloader(dirname_pattern='.', filename_pattern='{shortcode}')
static_dir = r'C:\Users\Dell\flow-kbeauty\static'
os.chdir(static_dir)

posts = [
    ('DYM-jYNE8SV', 'mini-blueberry-bliss'),
    ('DX4WHBXE3_3', 'golden-crunch-burger'),
    ('DXviAj_kwgL', 'classic-affogato'),
    ('DXt-HdME_zd', 'cold-kaapi-scoop'),
    ('DXrfKvxk49E', 'herbed-rice-chicken'),
    ('DXgTXPAk_Mq', 'potato-chicken-skewers'),
    ('DXUHTKzkwEV', 'chicken-marinara'),
    ('DXRncsGE3kM', 'classic-tiramisu'),
    ('DXQjscoE8Bx', 'pistachio-tiramisu'),
    ('DXOQd1-DXub', 'choco-hazelnut-tiramisu'),
    ('DYzPQJGk4-o', 'caramel-crunch'),
]

for shortcode, name in posts:
    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        print(f'{name}: {post.width}x{post.height}')
        L.download_post(post, target='.')
        for f in os.listdir('.'):
            if f.startswith(shortcode) and (f.endswith('.jpg') or f.endswith('.png') or f.endswith('.webp')):
                ext = f.split('.')[-1]
                newname = f'{name}.{ext}'
                if os.path.exists(newname):
                    os.remove(newname)
                os.rename(f, newname)
                print(f'  -> {newname}')
                break
    except Exception as e:
        print(f'ERR {name}: {e}')
