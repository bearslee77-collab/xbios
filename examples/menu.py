# MENU.PY - SCREEN 2 menu with two demos

def m():
    screen.mode(2)

def e():
    return key.pressed("ESC")

def w():
    while e(): pass
    key.flush()

def d1():
    m()
    sprite.size(8,True)
    sprite.pattern(0,chr(255)*8)
    for n in range(8):
        sprite.put(n,0,0,n+2,0)
    f=0
    while not e():
        o=0
        for n in range(8):
            p=(f+o)&255
            if p>127: p=255-p
            sprite.put(n,p+p,((f+f+o)&127)+40)
            o=o+29
        f=f+1
    sprite.clear()
    w()

def d2():
    m()
    i=0
    while not e():
        screen.circle(128,100,(i&63)+8,15)
        i=i+1
        if i&63==0: m()
    w()

while 1:
    m()
    screen.text(64,64,"1 BALLS")
    screen.text(64,88,"2 RINGS")
    screen.text(64,128,"ESC")
    k=key.get()
    if k=="1": d1()
    if k=="2": d2()
    if k==chr(27): break
screen.mode(0)
