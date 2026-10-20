# XWAVE.PY - plasma, sunset and rose curves (turbo R)

NS=10
HZ=104
SUNY=74
PART=150

sine=[]
cx=[]
cy=[]
pa=[]
pb=[]
r0=""
r1=""
cp=1
sc=0
lx=128
ly=96

def mk():
    for n in range(64):
        a=n*0.0981748
        sine.append(31+int(31*math.sin(a)))
        cx.append(120+int(112*math.sin(a)))
        cy.append(88+int(64*math.sin(a+a)))
    for v in [0,73,138,203,268,333,398,504,169,497,441,73,203,333,0,511]:
        pa.append(v)
    pb.append(0)
    for n in range(13):
        a=n*0.48332
        pb.append((4+int(3*math.sin(a)))*64+(4+int(3*math.sin(a+2.0944)))*8
                  +4+int(3*math.sin(a+4.18879)))
    pb.append(0)
    pb.append(511)

def pal(t):
    for n in range(1,16):
        if t==0:
            v=pb[n]
        else:
            v=pa[n]
        screen.palette(n,v>>6,v>>3&7,v&7)

def el(t):
    g=time.tick()-t
    if g<0:
        g=g+65536
    return g

def pat():
    sprite.size(16,False)
    sprite.clear()
    a=""
    b=""
    for r in range(16):
        h=r
        if h>7:
            h=15-h
        w=1
        n=h+h+2
        while n>0:
            w=w+w
            n=n-1
        w=w-1<<7-h
        a=a+chr(w>>8)
        b=b+chr(w&255)
    sprite.pattern(0,a+b)

def plasma():
    j=0
    while j<24:
        i=0
        while i<32:
            v=sine[(i+j)&63]+sine[(i+i)&63]+sine[(j*3)&63]
            screen.line(i*8,j*8,i*8+7,j*8+7,1+v//15,"BF")
            i=i+1
        j=j+1

def sunset():
    y=0
    for n in range(6):
        screen.line(0,y,255,y+17,n+1,"BF")
        y=y+18
    n=-40
    while n<40:
        w=int(math.sqrt(1600-n*n))
        screen.line(128-w,SUNY+n,128+w,SUNY+n,9)
        n=n+1
    n=6
    while n<40:
        y=SUNY+n
        screen.line(96,y,160,y+1,y//18+1,"BF")
        n=n+n//2+3
    screen.line(0,HZ,255,HZ+1,7,"BF")
    screen.line(0,HZ+2,255,211,1,"BF")
    n=-8
    while n<9:
        screen.line(128+n*8,HZ+2,128+n*30,211,8)
        n=n+1
    y=HZ+4
    n=2
    while y<211:
        screen.line(0,y,255,y,8)
        y=y+n
        n=n+n//2+1

def plot(p):
    global lx,ly
    r=20+sine[(p*15+(p>>3))&63]
    x=128+((sine[(p*3+16)&63]-31)*r>>5)
    y=96+((sine[(p*3)&63]-31)*r>>5)
    screen.line(lx,ly,x,y,1+(p>>3)%13)
    lx=x
    ly=y

def tick(p):
    if sc==2:
        plot(p)
    u=p
    v=p+p
    for n in range(NS):
        sprite.put(n,cx[u&63],cy[v&63])
        u=u+5
        v=v+7
    if sc==0:
        if p&1==0:
            q=p>>1
            for n in range(13):
                v=pb[1+(q+n)%13]
                screen.palette(n+1,v>>6,v>>3&7,v&7)
    elif sc==1:
        if p&3==0:
            q=p>>2
            for n in range(6):
                v=pa[1+(q+n)%6]
                screen.palette(n+1,v>>6,v>>3&7,v&7)

def bg():
    global lx,ly
    if sc==2:
        screen.color(15,14,14)
    else:
        screen.color(15,1,1)
    screen.mode(5)
    if sc==1:
        pal(1)
        sunset()
    else:
        pal(0)
        if sc==0:
            plasma()
        else:
            lx=128
            ly=96
    pat()
    for n in range(NS):
        sprite.put(n,0,208,11+n%3,0)

def show():
    global sc
    p=0
    bg()
    while True:
        tick(p)
        p=p+1
        if p%PART==0:
            sc=(sc+1)%3
            bg()
        if key.pressed("ESC"):
            return

def timed():
    global cp,r0,r1,sc
    sc=1
    bg()
    for Q in [0,2]:
        turbo.cpu(Q,True)
        cp=Q
        t=time.tick()
        for p in range(60):
            tick(p)
        g=el(t)
        c=0
        for p in range(60):
            u=p
            v=p+p
            for n in range(NS):
                c=c+cx[u&63]+cy[v&63]
                u=u+5
                v=v+7
        if Q==0:
            r0=" F"+str(g)+" C"+str(c)
        else:
            r1=" F"+str(g)+" C"+str(c)
    turbo.cpu(2,True)
    cp=1
    screen.mode(0)
    print("XPY XWAVE Q0"+r0)
    print("XPY XWAVE Q1"+r1)
    print("60 TICKS  HEAP "+str(sys.mem()[0]))
    print("THE TWO C MUST AGREE")
    print("PRESS A KEY")
    key.flush()
    key.get()

if sys.msx()<4:
    print("XWAVE WANTS A TURBO R")
else:
    mk()
    turbo.cpu(2,True)
    screen.color(15,1,1)
    screen.mode(5)
    pal(1)
    screen.text(64,52,"X W A V E",15)
    screen.text(24,84,"A KEY - RUN IT",9)
    screen.text(24,100,"T     - TIME IT",9)
    screen.text(24,132,"THREE PARTS AND THEY TURN",7)
    screen.text(24,144,"THEMSELVES.  ESC LEAVES.",7)
    k=key.get()
    if k=="t" or k=="T":
        timed()
    else:
        show()
    turbo.cpu(0,True)
    screen.mode(0)
