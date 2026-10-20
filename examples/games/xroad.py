# XROAD.PY - road game (MSX1)

MX=14
hx=[0,0,8,8,8,0,-8,-8,-8]
SPD=6
FLOOR=184
PY=168

DN=6
MKX=[60,164]
GRASS=2
ROAD=14
MARK=15

y=[]
xs=[]
dy=[]
for i in range(MX):
    y.append(0)
    xs.append(i*16+8)
for i in range(DN):
    dy.append(i*32)

def art():
    screen.color(15,ROAD,GRASS)
    screen.mode(2)
    screen.line(24,0,27,191,MARK,"BF")
    screen.line(228,0,231,191,MARK,"BF")
    sprite.size(8,True)
    sprite.pattern(0,chr(24)+chr(60)+chr(60)+chr(126)+chr(126)+chr(90)+chr(126)+chr(102))
    sprite.pattern(1,chr(102)+chr(126)+chr(90)+chr(126)+chr(126)+chr(60)+chr(60)+chr(24))

def road():
    for i in range(DN):
        v=dy[i]
        screen.line(MKX[0],v,MKX[0]+3,v+15,MARK,"BF")
        screen.line(MKX[1],v,MKX[1]+3,v+15,MARK,"BF")

def drop(i):
    global y
    y[i]=random.randint(0,120)
    sprite.put(i+1,xs[i],y[i],10,1)

def wave(n):
    global y
    for i in range(n):
        drop(i)
    i=n
    while i<MX:
        sprite.hide(i+1)
        i=i+1

def title():
    art()
    screen.text(48,40,"X R O A D")
    screen.text(24,72,"SPACE - DRIVE")
    screen.text(24,88,"B     - DEMO AND TIME IT")
    screen.text(16,128,"CURSOR OR STICK TO STEER")
    screen.text(16,144,"ESC TO QUIT")

def demo():
    global y
    art()
    random.seed(1)
    n=12
    wave(n)
    road()
    sprite.hide(0)
    c=0
    t=time.tick()
    for f in range(60):
        for i in range(n):
            b=y[i]+SPD
            if b>FLOOR:
                b=0
            y[i]=b
            c=c+b
            sprite.put(i+1,xs[i],b)
    g=time.tick()-t
    if g<0:
        g=g+65536
    screen.mode(0)
    print("XPY N="+str(n)+" F="+str(g)+" C="+str(c))
    print("60 TICKS OF "+str(n)+" CARS")
    print("PRESS A KEY")
    key.flush()
    key.get()

def play():
    global y
    art()
    sound.play("T160L16V13O4CEGO5C")
    n=4
    wave(n)
    road()
    px=112
    sprite.put(0,px,PY,15,0)
    sprite.collision()
    s=0
    t=time.tick()
    while True:
        u=hx[joy.stick(0)]
        if u!=0:
            px=px+u
            if px<24:
                px=24
            if px>216:
                px=216
            sprite.put(0,px,PY)
        for i in range(n):
            b=y[i]+SPD
            if b>FLOOR:
                b=0
            y[i]=b
            sprite.put(i+1,xs[i],b)
        if sprite.collision():
            sound.play("T100L8V15O3GEC")
            break
        if key.pressed("ESC"):
            return
        s=s+1
        if s%80==0:
            if n<MX:
                n=n+1
                drop(n-1)
                sound.play("T200L32V12O5CG")
    g=time.tick()-t
    if g<0:
        g=g+65536
    screen.text(8,8,"CRASH.  WAVE "+str(n)+" CARS")
    screen.text(8,24,"TICKS "+str(s)+"  FRAMES "+str(g))
    if g>0:
        screen.text(8,40,"TICKS PER 60 FRAMES "+str(s*60//g))
    screen.text(8,64,"PRESS A KEY")
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
