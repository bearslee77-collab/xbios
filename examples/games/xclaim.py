# XCLAIM.PY - claim the field (MSX2)

U=4
C=12
T=8
X=5
MX=5
MT=40
BY=191

sx=[0,0,2,2,2,0,-2,-2,-2]
sy=[0,-2,0,0,0,2,0,0,0]

tx=[]
ty=[]
for i in range(MT):
    tx.append(0)
    ty.append(0)

ex=[]
ey=[]
edx=[]
edy=[]
for i in range(MX):
    ex.append(0)
    ey.append(0)
    edx.append(2)
    edy.append(2)

px=8
py=0
pdx=0
pdy=0
dr=0
tn=0
en=2
lv=1
li=3
sc=0
pc=0
al=1

def pat(n,a,b):
    sprite.pattern(n,chr(a)+chr(b)+chr(b)+chr(b)+chr(a)+chr(0)+chr(0)+chr(0))

def art():
    screen.color(15,1,1)
    screen.mode(5)
    sprite.size(8,False)
    sprite.clear()
    pat(0,240,240)
    pat(1,112,248)

def spawn():
    for i in range(MX):
        ex[i]=40+i*40
        ey[i]=40+i*24
        edx[i]=2
        edy[i]=2
        if i%2==1:
            edx[i]=-2
    for i in range(en):
        sprite.put(i+1,ex[i],ey[i],10,1)

def seg(x1,y1,x2,y2,c):
    if y1==y2:
        screen.line(x1,y1,x2,y2+1,c,"BF")
    else:
        screen.line(x1,y1,x2+1,y2,c,"BF")

def pct():
    c=0
    a=16
    while a<256:
        b=12
        while b<192:
            if screen.point(a,b)==C:
                c=c+1
            b=b+24
        a=a+32
    return c

def hud():
    screen.line(0,192,255,211,1,"BF")
    screen.text(8,197,"LV"+str(lv)+" L"+str(li)+" "+str(pc*100//64)+"% "+str(sc),15)

def grab(a,b):
    if screen.point(a,b)!=U:
        return 0
    screen.paint(a,b,X,C)
    if screen.point(ex[0],ey[0])==X:
        screen.paint(a,b,U,C)
        return 0
    screen.paint(a,b,C,C)
    return 1

def close():
    global dr,sc,pc,tn
    tx[tn]=px
    ty[tn]=py
    tn=tn+1
    m=-1
    k=0
    i=0
    while i<tn-1:
        seg(tx[i],ty[i],tx[i+1],ty[i+1],C)
        d=abs(tx[i+1]-tx[i])+abs(ty[i+1]-ty[i])
        if d>m:
            m=d
            k=i
        i=i+1
    ax=(tx[k]+tx[k+1])//2
    ay=(ty[k]+ty[k+1])//2
    if ty[k]==ty[k+1]:
        qx=0
        qy=5
    else:
        qx=5
        qy=0
    if qx==0:
        if ey[0]>ay:
            qy=-5
    elif ex[0]>ax:
        qx=-5
    if grab(ax+qx,ay+qy)==0:
        grab(ax-qx,ay-qy)
    i=1
    while i<en:
        if screen.point(ex[i],ey[i])==C:
            ex[i]=ex[0]
            ey[i]=ey[0]
            sc=sc+50
        i=i+1
    dr=0
    n=pct()
    sc=sc+(n-pc)*10
    pc=n
    hud()

def hit():
    global li,dr,px,py,al
    if dr==1:
        tx[tn]=px
        ty[tn]=py
        i=0
        while i<tn:
            seg(tx[i],ty[i],tx[i+1],ty[i+1],U)
            i=i+1
        screen.line(tx[0]-3,ty[0]-3,tx[0]+3,ty[0]+3,C,"BF")
        px=tx[0]
        py=ty[0]
        dr=0
    li=li-1
    sprite.put(0,px,py)
    hud()
    if li<1:
        al=0

def step():
    global px,py,pdx,pdy,dr,tn
    s=joy.stick(0)
    if s==0:
        return
    u=sx[s]
    v=sy[s]
    a=px+u
    b=py+v
    if b>BY:
        return
    p=screen.point(a,b)
    if p<0:
        return
    if p==T:
        return
    if dr==1:
        if u!=pdx or v!=pdy:
            if tn>=MT-1:
                hit()
                return
            tx[tn]=px
            ty[tn]=py
            tn=tn+1
        seg(px,py,a,b,T)
    elif p==U:
        dr=1
        tx[0]=px
        ty[0]=py
        tn=1
        seg(px,py,a,b,T)
    pdx=u
    pdy=v
    px=a
    py=b
    sprite.put(0,a,b)
    if dr==1 and p==C:
        close()

def etick():
    for i in range(en):
        a=ex[i]+edx[i]
        b=ey[i]+edy[i]
        p=screen.point(a,b)
        if p==T:
            hit()
            return
        if p==U:
            ex[i]=a
            ey[i]=b
            sprite.put(i+1,a,b)
        else:
            if screen.point(a,ey[i])!=U:
                edx[i]=-edx[i]
            if screen.point(ex[i],b)!=U:
                edy[i]=-edy[i]

def title():
    art()
    screen.text(56,32,"X C L A I M",15)
    screen.text(24,72,"SPACE - PLAY",11)
    screen.text(24,88,"B     - DEMO AND TIME IT",11)
    screen.text(16,120,"CURSOR OR STICK TO MOVE",14)
    screen.text(16,136,"LEAVE THE WALL TO CUT THE FIELD",14)
    screen.text(16,152,"COME HOME TO KEEP THE HALF THEY",14)
    screen.text(16,168,"ARE NOT IN.  ESC TO QUIT",14)

def el(t):
    g=time.tick()-t
    if g<0:
        g=g+65536
    return g

def demo():
    global en
    art()
    en=4
    level()
    sprite.hide(0)
    c=0
    t=time.tick()
    for f in range(60):
        etick()
        for i in range(en):
            c=c+ex[i]+ey[i]
    g=el(t)
    screen.mode(0)
    print("XPY N="+str(en)+" F="+str(g)+" C="+str(c))
    print("60 TICKS OF "+str(en)+" OBJECTS")
    print("PRESS A KEY")
    key.flush()
    key.get()

def level():
    global px,py,dr,pc
    screen.line(0,0,255,BY,C,"BF")
    screen.line(4,4,251,BY-4,U,"BF")
    px=8
    py=0
    dr=0
    sprite.put(0,px,py,15,0)
    spawn()
    pc=pct()
    hud()

def play():
    global al,en,lv,li,sc
    lv=1
    li=3
    sc=0
    en=2
    al=1
    art()
    level()
    t=time.tick()
    while al==1:
        step()
        etick()
        if key.pressed("ESC"):
            return
        if pc>=48:
            lv=lv+1
            if en<MX:
                en=en+1
            level()
    screen.text(48,80,"OUT OF LIVES",15)
    screen.text(24,104,"LEVEL "+str(lv)+"   OBJECTS "+str(en),15)
    screen.text(24,120,"SCORE "+str(sc)+"   FRAMES "+str(el(t)),15)
    screen.text(24,148,"PRESS A KEY",8)
    key.flush()
    key.get()

title()
while True:
    k=key.get()
    if k==chr(27):
        break
    if k=="b" or k=="B":
        demo()
    else:
        play()
    title()
screen.mode(0)
