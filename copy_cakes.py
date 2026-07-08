import os, shutil

dl = r'C:\Users\Dell\Downloads'
static = r'C:\Users\Dell\flow-kbeauty\static'

files = sorted([f for f in os.listdir(dl) if f.startswith(('AQ','736'))])

for i, f in enumerate(files):
    src = os.path.join(dl, f)
    ext = 'jpg' if f.endswith(('jpeg','jpg')) else 'mp4'
    name = f'cake-{i+1}.{ext}'
    dst = os.path.join(static, name)
    shutil.copy2(src, dst)
    print(f'{name}: {os.path.getsize(dst)//1024}KB')
