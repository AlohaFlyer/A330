#!/usr/bin/env python3
"""Poster-mode image for flows_quiz.html: same crops and layout as build_cockpit_image.py, rendered at DPI
(default 480) onto a W (default 4800) px canvas, JPEG q85 -> assets/a330_cockpit_hi.jpg. The PDF is vector,
so raise DPI/W for more detail. The 1200 px a330_cockpit.jpg stays the map background."""
import subprocess, os
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
DPI=int(os.environ.get('DPI','480')); W=int(os.environ.get('W','4800'))
subprocess.run(['pdftoppm','-r',str(DPI),'-png',os.path.join(os.path.dirname(os.path.abspath(__file__)),'src','A330 All Panels FULL SIZE.pdf'),'/tmp/a330_poster'],check=True)
im=Image.open('/tmp/a330_poster-1.png').convert('RGB'); s=im.size[0]/796
crop=lambda a,b,c,d: im.crop((int(a*s),int(b*s),int(c*s),int(d*s)))
oh=crop(276,6,524,480); mp=crop(20,484,778,730); pd=crop(288,732,510,1100)
k=W/1200; H=round(W*437/300); gap=round(12*k)
fh=lambda i,h: i.resize((round(i.width*h/i.height),h),Image.LANCZOS)
fw=lambda i,w: i.resize((w,round(i.height*w/i.width)),Image.LANCZOS)
oh2=fh(oh,round(720*k)); mp2=fw(mp,W); pd2=fh(pd,H-oh2.height-mp2.height-3*gap)
c=Image.new('RGB',(W,H),(255,255,255)); y=gap
c.paste(oh2,((W-oh2.width)//2,y)); y+=oh2.height+gap; c.paste(mp2,(0,y)); y+=mp2.height+gap; c.paste(pd2,((W-pd2.width)//2,y))
c.save(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','assets','a330_cockpit_hi.jpg'),quality=85,optimize=True,progressive=True)
print(c.size, os.path.getsize(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','assets','a330_cockpit_hi.jpg')))
