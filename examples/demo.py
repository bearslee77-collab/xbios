# DEMO.PY - XPY demo cartridge: menu and four demos

def m():
    screen.mode(2)

def e():
    return key.pressed("ESC")

def w():
    while e(): pass
    key.flush()

def s(L):
    m()
    y=8
    for t in L:
        screen.text(4,y,t)
        y=y+9
    return key.get()

def d1():
    m()
    screen.text(72,24,"HELLO")
    i=0
    while not e():
        c=(i&7)+1
        screen.line(8+i,60,8+i,180,c)
        screen.line(247-i,60,247-i,180,c)
        i=i+1
        if i>119: i=0
    w()

def d2():
    m()
    sprite.size(8,True)
    sprite.pattern(0,chr(255)*8)
    for n in range(16):
        sprite.put(n,0,0,(n%14)+2,0)
    a=0
    b=0
    while not e():
        a=(a+6)&511
        p=a
        if p>255: p=511-p
        r=255-p
        b=(b+10)&511
        q=b
        if q>255: q=511-q
        t=255-q
        sprite.put(0,p,20)
        sprite.put(1,q,30)
        sprite.put(2,r,40)
        sprite.put(3,t,50)
        sprite.put(4,q,60)
        sprite.put(5,p,70)
        sprite.put(6,t,80)
        sprite.put(7,r,90)
        sprite.put(8,r,100)
        sprite.put(9,t,110)
        sprite.put(10,p,120)
        sprite.put(11,q,130)
        sprite.put(12,t,140)
        sprite.put(13,r,150)
        sprite.put(14,q,160)
        sprite.put(15,p,170)
    sprite.clear()
    w()

def d3():
    screen.mode(5)
    screen.text(88,4,"FRACTAL")
    for x in range(80):
        if e(): break
        a=x*10-563
        g=x+88
        for y in range(32):
            if e(): break
            b=y*10
            r=0
            i=0
            j=8
            for n in range(8):
                u=(r*r)>>8
                v=(i*i)>>8
                if u+v>1024:
                    j=n
                    break
                i=((r*i)>>7)+b
                r=u-v+a
            c=j+4
            screen.pset(g,106+y,c)
            screen.pset(g,105-y,c)
    while not e(): pass
    w()

def d4():
    m()
    i=0
    while not e():
        r=(i&63)+8
        screen.circle(128,96,r,15)
        i=i+1
        if i&63==0: m()
    w()

while 1:
    k=s(["XPY DEMO","1 HELLO","2 BALLS","3 FRACTAL","4 RINGS"])
    if k=="1": d1()
    if k=="2": d2()
    if k=="3": d3()
    if k=="4": d4()
    if k==chr(27): break
screen.mode(0)
