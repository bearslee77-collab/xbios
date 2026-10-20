# XROTO.PY - rotozoom (turbo R)

X0=64
Y0=58
W=128
H=96
COS=[256,255,251,245,237,226,213,198,181,162,142,121,98,74,50,25,0]
ZOOM=[96,112,128,160,192,224,256,288,320,352,384,352,320,288,256,224,192,160,128,112]
PR=[7,7,7,7,5,3,1,0,0,0,1,3,5,7,7]
PG=[0,2,4,6,7,7,7,7,5,3,1,0,0,0,0]
PB=[3,1,0,0,0,0,1,3,5,7,7,7,7,6,4]
tx=""
cp=1
ly=1
r0=""
r1=""
r2=""
r3=""

def cos64(a):
    a=a&63
    q=a>>4
    r=a&15
    if q==0:
        return COS[r]
    if q==1:
        return -COS[16-r]
    if q==2:
        return -COS[r]
    return COS[16-r]

def sin64(a):
    return cos64(a-16)

def mk():
    global tx
    s=""
    for v in range(16):
        for u in range(16):
            d=(u-8)*(u-8)+(v-8)*(v-8)
            c=1+(((d>>2)+((u^v)&1)*7)%15)
            s=s+chr(c)
    for v in range(16):
        for u in range(16):
            s=s+chr((abs(u-8)+abs(v-8))&15)
    tx=s

def pal():
    for n in range(15):
        screen.palette(n+1,PR[n],PG[n],PB[n])

def el(t):
    g=time.tick()-t
    if g<0:
        g=g+65536
    return g

def tick(p):
    z=ZOOM[p%20]
    c=(cos64(p)*z)>>8
    s=(sin64(p)*z)>>8
    u=(p*96+131072-64*c+48*s)&65535
    v=(p*64+131072-64*s-48*c)&65535
    screen.rotozoom(tx,X0,Y0,W,H,u,v,c,s)

def tick2(p):
    z=ZOOM[p%20]
    c=(cos64(p)*z)>>8
    s=(sin64(p)*z)>>8
    u=(p*96+131072-64*c+48*s)&65535
    v=(p*64+131072-64*s-48*c)&65535
    a=(640-p*2)&63
    z=ZOOM[(p+10)%20]
    c2=(cos64(a)*z)>>8
    s2=(sin64(a)*z)>>8
    u2=(131072-p*48-64*c2+48*s2)&65535
    v2=(131072+p*80-64*s2-48*c2)&65535
    screen.rotozoom(tx,X0,Y0,W,H,u,v,c,s,u2,v2,c2,s2)

def frame():
    screen.line(X0-2,Y0-2,X0+W+1,Y0+H+1,15,"B")
    screen.line(X0-1,Y0-1,X0+W,Y0+H,7,"B")

def show():
    global cp,ly
    p=0
    screen.cls()
    frame()
    while True:
        if ly==2:
            tick2(p)
        else:
            tick(p)
        p=p+1
        if key.pressed("ESC"):
            return
        if key.pressed("SPACE"):
            cp=2-cp
            turbo.cpu(cp,True)
            while key.pressed("SPACE"):
                pass
        if key.pressed("RETURN"):
            ly=3-ly
            while key.pressed("RETURN"):
                pass

def timed():
    global cp,r0,r1,r2,r3
    frame()
    for L in [1,2]:
        for Q in [0,2]:
            turbo.cpu(Q,True)
            cp=Q
            c=0
            t=time.tick()
            for p in range(60):
                if L==1:
                    tick(p)
                else:
                    tick2(p)
                z=ZOOM[p%20]
                a=(cos64(p)*z)>>8
                b=(sin64(p)*z)>>8
                c=c+screen.vpeek(Y0*128+X0//2)
                c=c+screen.vpeek(Y0*128+(X0+W-2)//2)
                c=c+screen.vpeek((Y0+H-1)*128+X0//2)
                c=c+screen.vpeek((Y0+H-1)*128+(X0+W-2)//2)
                c=c+screen.vpeek((Y0+48)*128+(X0+64)//2)
                c=c+((a+b+(-b)+a)&65535)
            g=" F"+str(el(t))+" C"+str(c)
            if L==1 and Q==0:
                r0=g
            if L==1 and Q==2:
                r1=g
            if L==2 and Q==0:
                r2=g
            if L==2 and Q==2:
                r3=g
    turbo.cpu(2,True)
    cp=2
    screen.mode(0)
    print("XPY XROTO Q0"+r0)
    print("XPY XROTO Q1"+r1)
    print("XPY XROTO 2 Q0"+r2)
    print("XPY XROTO 2 Q1"+r3)
    print("60 TICKS  HEAP "+str(sys.mem()[0]))
    print("EACH PAIR OF C MUST AGREE")
    print("PRESS A KEY")
    key.flush()
    key.get()

if sys.msx()<4:
    print("XROTO WANTS A TURBO R")
else:
    mk()
    turbo.cpu(2,True)
    screen.color(15,0,0)
    screen.mode(5)
    pal()
    screen.text(64,52,"X R O T O",15)
    screen.text(24,84,"A KEY - RUN IT",9)
    screen.text(24,100,"T     - TIME IT",9)
    screen.text(24,132,"A TEXTURE, TURNED AND ZOOMED.",7)
    screen.text(24,144,"RETURN: TWO TEXTURES AT ONCE.",7)
    screen.text(24,156,"SPACE: THE CPU.  ESC LEAVES.",7)
    k=key.get()
    if k=="t" or k=="T":
        timed()
    else:
        show()
    turbo.cpu(0,True)
    screen.mode(0)
