# Usage (run inside a lander folder): python3 embed.py <name>-standalone.html
# Creates a standalone html: every image (local + remote) embedded as data URI -> works anywhere, no folders, no external links
import re, base64, io, os, urllib.request, hashlib
from PIL import Image
import sys
OUTNAME=sys.argv[1] if len(sys.argv)>1 else 'standalone.html'
src=open('index.html',encoding='utf-8').read()
cache={}
def to_data(img_bytes, name, maxw):
    ext=name.lower().rsplit('.',1)[-1].split('?')[0]
    if ext in ('svg',):
        return 'data:image/svg+xml;base64,'+base64.b64encode(img_bytes).decode()
    im=Image.open(io.BytesIO(img_bytes))
    if getattr(im,'is_animated',False):  # keep animations as-is (webp/gif)
        mime='image/webp' if ext=='webp' else 'image/gif'
        return f'data:{mime};base64,'+base64.b64encode(img_bytes).decode()
    im=im.convert('RGBA') if im.mode in ('RGBA','LA','P') else im.convert('RGB')
    if im.width>maxw: im=im.resize((maxw,int(im.height*maxw/im.width)),Image.LANCZOS)
    b=io.BytesIO(); im.save(b,'WEBP',quality=80,method=6)
    return 'data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
def fetch(u):
    req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124 Safari/537.36'})
    return urllib.request.urlopen(req,timeout=40).read()
def maxw_for(u):
    n=u.lower()
    if 'review-' in n: return 420
    if 'avatar' in n or 'sticky' in n: return 160
    if 'paket-' in n: return 520
    if 'logo' in n: return 400
    if any(k in n for k in ('flag','trustpilot','wrinkolex','tp-','check','icon','images.png','5%20star','customer')): return 300
    return 820
def repl(m):
    u=m.group(2)
    if u.startswith('data:'): return m.group(0)
    if u not in cache:
        try:
            data=open(u,'rb').read() if not u.startswith('http') else fetch(u)
            cache[u]=to_data(data,u,maxw_for(u))
        except Exception as e:
            print('FAILED',u,e); cache[u]=u
    return m.group(1)+cache[u]+m.group(3)
out=re.sub(r'(<img[^>]*?\ssrc=")([^"]+)(")',repl,src)
# embed Poppins so typography matches without Google Fonts
fonts=''
for w,f in [(400,'Regular'),(500,'Medium'),(600,'SemiBold'),(700,'Bold')]:
    p=f'/tmp/fonts/Poppins-{f}.ttf'
    if os.path.exists(p):
        fonts+="@font-face{font-family:'Poppins';font-weight:%d;font-style:normal;font-display:swap;src:url(data:font/ttf;base64,%s) format('truetype')}\n"%(w,base64.b64encode(open(p,'rb').read()).decode())
out=out.replace('<style>','<style>\n'+fonts,1)
out=out.replace('loading="lazy"','')
open(OUTNAME,'w',encoding='utf-8').write(out)
left=re.findall(r'<img[^>]*?\ssrc="(http[^"]+)"',out)
print('images embedded:',len(cache),'| remaining external img:',len(left),'| size MB:',round(len(out)/1e6,2))
