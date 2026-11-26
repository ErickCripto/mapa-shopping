import math, sys
from PIL import Image, ImageDraw, ImageFilter
W,H=150,130; S=3; OX,OY=20,30
class TD:
    def __init__(s,im): s.d=ImageDraw.Draw(im)
    def _p(s,ps): return [(x+OX,y+OY) for x,y in ps]
    def ellipse(s,b,**k): s.d.ellipse([b[0]+OX,b[1]+OY,b[2]+OX,b[3]+OY],**k)
    def polygon(s,ps,**k): s.d.polygon(s._p(ps),**k)
    def line(s,ps,**k): s.d.line(s._p(ps),**k)
    def point(s,p,**k): s.d.point((p[0]+OX,p[1]+OY),**k)
    def text(s,p,t,**k): s.d.text((p[0]+OX,p[1]+OY),t,**k)

C=dict(fur=(150,132,116),furl=(186,170,152),furd=(112,96,84),head=(198,188,174),headd=(160,148,134),
 rear=(84,70,64),blk=(28,24,28),wht=(246,242,232),leg=(232,226,214),legd=(196,188,174),claw=(214,190,150),
 tail=(92,80,74),taill=(138,124,112),pink=(240,120,140),blush=(236,150,150),eye=(20,18,24),blue=(37,99,235),neon=(57,255,122),outl=(30,22,26))
def rot(p,c,a):
    a=math.radians(a); x,y=p[0]-c[0],p[1]-c[1]
    return (c[0]+x*math.cos(a)-y*math.sin(a), c[1]+x*math.sin(a)+y*math.cos(a))
def ell(d,cx,cy,rx,ry,col): d.ellipse([cx-rx,cy-ry,cx+rx,cy+ry],fill=col)
def bez(p0,p1,p2,t): return tuple((1-t)**2*p0[i]+2*(1-t)*t*p1[i]+t*t*p2[i] for i in (0,1))

def frame(dy=0,tail=0,head=0,lift=0,lift2=0,tongue=0,eye='open',fx=None,t=0,hop=0):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=TD(im)
    G=84  # chão
    by=50+dy-hop
    # ---- cauda (bandeira), atrás de tudo
    base=(78,by-4); tip=rot((100,by-40),base,tail); ctrl=rot((98,by-10),base,tail*0.6)
    for i in range(15):
        u=i/14; p=bez(base,ctrl,tip,u); r=5+11*math.sin(math.pi*min(u*1.1,1))**0.8
        ell(d,p[0],p[1],r,r*0.9,C['tail'])
    for i in range(22):  # tufos de pelo nas bordas
        u=0.1+i/23; p=bez(base,ctrl,tip,u); q=bez(base,ctrl,tip,min(u+0.05,1))
        tx,ty=q[0]-p[0],q[1]-p[1]; L=math.hypot(tx,ty) or 1; nx,ny=-ty/L,tx/L
        r=5+11*math.sin(math.pi*min(u*1.1,1))**0.8
        for sgn in (1,-1):
            a=(p[0]+nx*r*0.8*sgn,p[1]+ny*r*0.8*sgn); b=(a[0]+nx*4*sgn+tx/L*3,a[1]+ny*4*sgn+ty/L*3)
            d.line([a,b],fill=C['tail'],width=2)
    for i in range(16):
        u=0.15+i/19; p=bez(base,ctrl,tip,u); q=bez(base,ctrl,tip,min(u+0.12,1)); off=((i%3)-1)*4
        d.line([(p[0]+off,p[1]+off*0.3),(q[0]+off,q[1]+off*0.3)],fill=C['taill'],width=1)
    tp=bez(base,ctrl,tip,1); 
    for k in (-3,0,3): d.line([tp,(tp[0]+k*1.5+(tip[0]-ctrl[0])*0.15,tp[1]-5+abs(k))],fill=C['tail'],width=2)
    # ---- pernas de trás
    for x,o in ((70,-1),(83,0)):
        d.polygon([(x-5,by+4),(x+5,by+4),(x+4+o,G-2-hop),(x-4+o,G-2-hop)],fill=C['rear']); d.line([(x+3,by+8),(x+3+o,G-4-hop)],fill=(64,52,48),width=1)
        ell(d,x+o,G-2-hop,5,2,C['rear'])
    # ---- perna da frente de trás (mais escura)
    def front(x,lft,col,cold,far=False):
        sh=(x,by+2)
        if lft:
            paw=rot((x,G-3-hop),sh,-lft)
        else: paw=(x-1,G-3-hop)
        d.line([sh,paw],fill=col,width=9)
        # faixa preta no punho
        bp=(sh[0]+(paw[0]-sh[0])*0.72, sh[1]+(paw[1]-sh[1])*0.72)
        ell(d,bp[0],bp[1],4.5,3,C['blk'])
        ell(d,paw[0],paw[1],5,3,col)
        # garras
        dx=paw[0]-sh[0]; dyy=paw[1]-sh[1]; L=math.hypot(dx,dyy); ux,uy=dx/L,dyy/L
        for k in (-2,0,2):
            a=(paw[0]+ux*2+(-uy)*k, paw[1]+uy*2+ux*k); b=(a[0]+ux*3-1.5*(1 if not lft else 0), a[1]+uy*3)
            d.line([a,b],fill=C['claw'],width=1)
    front(48,lift2,C['legd'],C['legd'])
    # ---- corpo
    ell(d,62,by,25,15,C['fur'])
    ell(d,76,by+1,13,13,C['rear'])
    ell(d,62,by+8,22,6,C['furd'])
    ell(d,58,by-7,16,5,C['furl'])
    # ---- pescoço + cabeça (gira em torno do pescoço)
    nk=(42,by-2)
    def R(p): return rot(p,nk,head)
    d.polygon([R(p) for p in [(48,by-12),(50,by+10),(34,by+6),(30,by-8)]],fill=C['head'])
    ell(d,*R((31,by-5)),9,8,C['head'])
    # focinho longo e tubular (levemente curvado p/ baixo)
    sn=[(26,by-10),(14,by-7),(4,by-3),(1,by-1),(2,by+1),(6,by+1),(16,by-1),(28,by+2)]
    d.polygon([R(p) for p in sn],fill=C['head'])
    d.polygon([R(p) for p in [(26,by-2),(16,by-1),(6,by+1),(3,by+1),(16,by+1),(28,by+2)]],fill=C['headd'])
    ell(d,*R((2,by)),1.5,1.5,C['blk'])  # narizinho
    # língua
    if tongue:
        pts=[R((2-i*1.2,by+1+math.sin(i*0.6+t)*1.8+i*0.35)) for i in range(tongue)]
        if len(pts)>1: d.line(pts,fill=C['pink'],width=2)
    # orelha
    ell(d,*R((37,by-12)),3,3,C['headd']); ell(d,*R((37,by-12)),1.5,1.5,C['furd'])
    # ---- FAIXA: preta com borda branca, do pescoço/garganta até o meio das costas
    lay=Image.new('L',(W,H),0); ld=TD(lay)
    ell(ld,62,by,25,15,255); ld.polygon([(48,by-12),(50,by+10),(36,by+6),(36,by-8)],fill=255)
    st=Image.new('RGBA',(W,H),(0,0,0,0)); sd=TD(st)
    def band(off,w,col):
        a=(38+off,by+12); b=(72+off,by-17)
        sd.line([a,b],fill=col,width=w)
    band(0,13,C['wht']); band(0,7,C['blk'])
    im.paste(st,(0,0),Image.composite(st.getchannel('A'),Image.new('L',(W,H),0),lay))
    d=TD(im)
    # perna da frente (perto), branca com punho preto e garras
    front(46,lift,C['leg'],C['legd'])
    # ---- olho
    e=R((30,by-6))
    if eye=='open':
        ell(d,e[0],e[1],3,3.4,C['eye']); ell(d,e[0]-1.2,e[1]-1.4,0.8,0.8,(255,255,255))
    elif eye=='happy':
        d.line([(e[0]-3,e[1]+1),(e[0],e[1]-2),(e[0]+3,e[1]+1)],fill=C['eye'],width=1)
    elif eye=='sad':
        ell(d,e[0],e[1]+1,2.4,2.4,C['eye']); d.point((round(e[0]-1),round(e[1])),fill=(255,255,255))
        d.line([(e[0]-3,e[1]-3),(e[0]+3,e[1]-5)],fill=C['eye'],width=1)
    elif eye=='wide':
        ell(d,e[0],e[1],3.2,3.4,(255,255,255)); ell(d,e[0],e[1],1.6,1.8,C['eye'])
    elif eye=='closed':
        d.line([(e[0]-3,e[1]),(e[0]+3,e[1])],fill=C['eye'],width=1)
    b=R((27,by-1)); ell(d,b[0],b[1],2.5,1.3,C['blush'])
    # lenço azul do app no pescoço
    # ---- contorno
    a=im.getchannel('A').point(lambda v:255 if v>0 else 0); im.putalpha(a)
    o=a.filter(ImageFilter.MaxFilter(3)); out=Image.new('RGBA',(W,H),C['outl']+(255,)); out.putalpha(o)
    out.alpha_composite(im); im=out; d=TD(im)
    if fx: fx(d,t)
    return im

def sweat(d,t): ell(d,40,22+(t%3),2,3,(127,200,255)); d.point((40,18+(t%3)),fill=(127,200,255))
def tear(d,t): ell(d,31,54+t%6,1.2,2,(127,200,255))
def think(d,t):
    for i,(x,y,r) in enumerate([(30,26,2),(34,19,3),(42,10,6)]):
        if t%6>=i: ell(d,x,y,r+1,r+1,C['outl']); ell(d,x,y,r,r,(255,255,255))
    if t%6>=2: d.text((40,4),'?',fill=C['blue'])
def spark(d,t):
    for i,(x,y) in enumerate([(14,20),(34,10),(56,6),(10,36)]):
        if (t+i)%3!=0:
            c=C['neon'] if i%2 else (255,210,60)
            d.line([(x-2,y),(x+2,y)],fill=c); d.line([(x,y-2),(x,y+2)],fill=c)
def pin(d,t):
    y=16-(1 if t%4<2 else 0)
    ell(d,14,y,5,5,C['outl']); ell(d,14,y,4,4,C['blue']); d.polygon([(10,y+2),(18,y+2),(14,y+9)],fill=C['blue']); ell(d,14,y,1.5,1.5,(255,255,255))
def notes(d,t):
    x=20+(t%6); y=18-(t%6)
    d.line([(x,y),(x,y-6)],fill=C['blue']); ell(d,x-1,y,2,1.5,C['blue']); d.line([(x,y-6),(x+3,y-4)],fill=C['blue'])

N=8; sn=lambda k,a=1:a*math.sin(2*math.pi*k/N)
P={
 'oi':      lambda k: frame(dy=round(sn(k,1)),tail=sn(k,6),lift=-60+sn(k,25),tongue=0,eye='happy' if k in(3,4) else 'open',t=k),
 'rota':    lambda k: frame(dy=-abs(round(sn(k,2))),tail=sn(k,8),lift=sn(k,25),lift2=-sn(k,25),eye='open',fx=pin,t=k),
 'ops':     lambda k: frame(dy=round(sn(k*2,1)),tail=-8+sn(k,3),head=4,lift=-15,eye='wide',fx=sweat,t=k),
 'chegou':  lambda k: frame(hop=round(abs(sn(k,5))),tail=sn(k,12),lift=-40,lift2=-25,tongue=6+k%4,eye='happy',fx=spark,t=k),
 'pensando':lambda k: frame(dy=0,tail=sn(k,3),head=-6,lift=-95,eye='closed' if k==5 else 'open',fx=think,t=k),
 'apontar': lambda k: frame(dy=round(sn(k,1)),tail=sn(k,4),lift=-75+sn(k,6),eye='open',t=k),
 'triste':  lambda k: frame(dy=1,tail=40+sn(k,2),head=10,eye='sad',fx=tear,t=k),
 'danca':   lambda k: frame(hop=round(abs(sn(k,4))),tail=sn(k,22),head=sn(k,8),lift=-45+sn(k,30),lift2=-45-sn(k,30),tongue=5,eye='happy',fx=notes,t=k),
}
out=sys.argv[1]
poses=list(P)
sheet=Image.new('RGBA',((W*S+12)*4+12,(H*S+12)*2+12),(236,240,246,255))
ALL={p:[P[p](k) for k in range(N)] for p in poses}
bb=None
for p in poses:
    for f in ALL[p]:
        b=f.getbbox(); bb=b if bb is None else (min(bb[0],b[0]),min(bb[1],b[1]),max(bb[2],b[2]),max(bb[3],b[3]))
bb=(bb[0]-2,bb[1]-2,bb[2]+2,bb[3]+2); CW,CH=bb[2]-bb[0],bb[3]-bb[1]; print('crop',bb,CW,CH)
sheet=Image.new('RGBA',((CW*S+12)*4+12,(CH*S+12)*2+12),(236,240,246,255))
for i,p in enumerate(poses):
    fr=[f.crop(bb).resize((CW*S,CH*S),Image.NEAREST) for f in ALL[p]]
    fr[0].save(f'{out}/bandi-{p}.webp',save_all=True,append_images=fr[1:],duration=130,loop=0,lossless=True)
    sheet.alpha_composite(fr[2],(12+(i%4)*(CW*S+12),12+(i//4)*(CH*S+12)))
sheet.save(f'{out}/poses.png')
