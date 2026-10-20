# XSHOT.PY - horizontal shooter (turbo R)

NB=10
SHOT=11
SHX=16

BT=48
BB=166
ly=[56,70,84,98,112,126,140,154]

HIT=14
NEAR=8
RNG=48

pl=[0,1,10,2,74,3,9,504,511,300,236,172,108,448,0,511]

bx=[]
bl=[]
bv=[]
kx=0
kl=0
sl=3
sy=3
hit=0
pop=0
cp=1
r0=""
r1=""

def mk():
    for i in range(NB):
        bx.append(0)
        bl.append(0)
        bv.append(0)

SHIP=chr(96)+chr(120)+chr(126)+chr(255)+chr(255)+chr(126)+chr(120)+chr(96)
BUBL=chr(60)+chr(66)+chr(129)+chr(129)+chr(129)+chr(129)+chr(66)+chr(60)
DART=chr(0)+chr(0)+chr(24)+chr(255)+chr(255)+chr(24)+chr(0)+chr(0)

def art():
    screen.color(15,14,14)
    screen.mode(5)
    for n in range(1,16):
        v=pl[n]
        screen.palette(n,v>>6,v>>3&7,v&7)
    n=0
    while n<64:
        screen.line(n*4,BT,n*4+3,BB,1+(n*5)%6,"BF")
        n=n+1
    sprite.size(8,False)
    sprite.clear()
    sprite.pattern(0,SHIP)
    sprite.pattern(1,BUBL)
    sprite.pattern(2,DART)

def el(t):
    g=time.tick()-t
    if g<0:
        g=g+65536
    return g

def spawn(i,p):
    bx[i]=232+(i%3)*8
    bl[i]=(p*3+i*5)%8
    bv[i]=3+(p+i*7)%5

def start():
    global kx,sl,pop,hit
    for i in range(NB):
        spawn(i,i*11)
        bx[i]=40+i*22
    kx=0
    sl=3
    pop=0
    hit=0
    sprite.put(0,SHX,ly[sl],7,0)
    for i in range(NB):
        sprite.put(i+1,bx[i],ly[bl[i]],9+i%4,1)
    sprite.put(SHOT,0,208,8,2)

def tick(p):
    global kx,kl,sl,pop,hit
    na=sl-1
    if na<0:
        na=1
    nb=sl+1
    if nb>7:
        nb=6
    d0=999
    d1=999
    d2=999
    for i in range(NB):
        x=bx[i]-bv[i]
        if x<8:
            spawn(i,p+i)
            x=bx[i]
        bx[i]=x
        b=bl[i]
        sprite.put(i+1,x,ly[b])
        if x<100:
            e=x-SHX
            if b==sl:
                if e<d0:
                    d0=e
            elif b==na:
                if e<d1:
                    d1=e
            elif b==nb:
                if e<d2:
                    d2=e
    if kx>0:
        kx=kx+12
        if kx>248:
            kx=0
            sprite.put(SHOT,0,208)
        else:
            sprite.put(SHOT,kx,ly[kl])
            for i in range(NB):
                if bl[i]==kl:
                    e=bx[i]-kx
                    if e>-NEAR:
                        if e<NEAR:
                            pop=pop+1
                            spawn(i,p+i+3)
                            sprite.put(i+1,bx[i],ly[bl[i]])
                            kx=0
                            sprite.put(SHOT,0,208)
    elif p&3==0:
        kx=SHX+16
        kl=sl
    if d0<RNG:
        if d1>d2:
            sl=na
        else:
            sl=nb
    if d0<HIT:
        hit=1
        sprite.put(0,SHX,ly[sl],13,0)
    else:
        if hit==1:
            hit=0
            sprite.put(0,SHX,ly[sl],7,0)
        else:
            sprite.put(0,SHX,ly[sl])
    if p&1==0:
        q=p>>1
        for n in range(6):
            v=pl[1+(q+n)%6]
            screen.palette(n+1,v>>6,v>>3&7,v&7)

def show():
    art()
    start()
    p=0
    while True:
        tick(p)
        p=p+1
        if key.pressed("ESC"):
            return

def timed():
    global cp,r0,r1
    art()
    for Q in [0,2]:
        turbo.cpu(Q,True)
        cp=Q
        start()
        t=time.tick()
        for p in range(60):
            tick(p)
        g=el(t)
        c=pop*1000+sl
        for i in range(NB):
            c=c+bx[i]+bl[i]*7
        if Q==0:
            r0=" F"+str(g)+" C"+str(c)
        else:
            r1=" F"+str(g)+" C"+str(c)
    turbo.cpu(2,True)
    cp=1
    screen.mode(0)
    print("XPY XSHOT Q0"+r0)
    print("XPY XSHOT Q1"+r1)
    print("60 TICKS  HEAP "+str(sys.mem()[0]))
    print("THE TWO C MUST AGREE")
    print("PRESS A KEY")
    key.flush()
    key.get()

if sys.msx()<4:
    print("XSHOT WANTS A TURBO R")
else:
    mk()
    turbo.cpu(2,True)
    screen.color(15,14,14)
    screen.mode(5)
    for n in range(1,16):
        v=pl[n]
        screen.palette(n,v>>6,v>>3&7,v&7)
    screen.text(56,52,"X S H O T",15)
    screen.text(24,84,"A KEY - RUN IT",9)
    screen.text(24,100,"T     - TIME IT",9)
    screen.text(24,132,"IT FLIES ITSELF.",7)
    screen.text(24,144,"ESC LEAVES.",7)
    k=key.get()
    if k=="t" or k=="T":
        timed()
    else:
        show()
    turbo.cpu(0,True)
    screen.mode(0)
