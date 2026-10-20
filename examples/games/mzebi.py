# MZEBI.PY - vertical shooter (MSX2)

C0=11
CW=10
FR=21
XL=C0*8
XR=(C0+CW)*8-8
XW=CW*8-8
RIVC=13
RDC=18
FC=[0,1,3,4,5,6,8,9]
NT=6
NE=4
TOP=40
BOT=168
SGH=32

GC=60
RC=92
DC=236
OC=17

PLAIN="\0"*8
TUFT="\0\0\x24\0\0\0\x42\0"
SCRUB="\0\x42\0\x18\0\x81\0\x24"
SOLID="\xff"*8
gp=[PLAIN,TUFT,SCRUB,SOLID]
gi=[0,1,3,1,2,0,1,3,2,1]
gc=[GC,GC,RC,GC,GC,GC,GC,DC,GC,GC]
GROW=""
CROW=""
for c in range(CW):
    GROW=GROW+gp[gi[c]]
    CROW=CROW+chr(gc[c])*8

hx=[0,0,8,8,8,0,-8,-8,-8]
hy=[0,-8,-8,0,8,8,8,0,-8]

TREE="\0\x18\x3c\x7e\x7e\x3c\x18\x18"
DOME="\0\0\x3c\x7e\xff\xff\xff\0"
PYR="\0\x18\x18\x3c\x3c\x7e\xff\0"
NAZ="\0\x42\x24\xff\x24\x18\x18\0"
tp=[TREE,DOME,PYR,NAZ]
ti=[GC,252,188,236]

SOLV="\x18\x3c\x3c\xff\xff\x3c\x66\xc3"
TORO="\x3c\x7e\xe7\xc3\xc3\xe7\x7e\x3c"
SITE="\xc3\x81\0\x18\x18\0\x81\xc3"
ZAP="\x18"*4+"\0"*4
BURST="\0\x24\x18\x7e\x7e\x18\x24\0"

tc=[C0]*NT
tr=[0]*NT
tt=[0]*NT
ex=[0]*NE
ey=[0]*NE

px=120
py=BOT
zx=0
zy=0
bx=0
bg=0
bs=0
sc=0
lv=3
hs=0
sp=4
iv=0
eb=[0]*NE

def art():
    screen.color(15,1,1)
    screen.mode(2)
    screen.vfill(8192,6144,OC)
    r=0
    while r<22:
        a=r*256+XL
        screen.vwrite(a,GROW)
        screen.vwrite(8192+a,CROW)
        r=r+1
    sprite.size(8,False)
    sprite.clear()
    sprite.pattern(0,SOLV)
    sprite.pattern(1,TORO)
    sprite.pattern(2,SITE)
    sprite.pattern(3,ZAP)
    sprite.pattern(4,BURST)

def feed(i):
    c=FC[(tc[i]+i*3+1)%8]
    tc[i]=C0+c
    tr[i]=0
    k=(c+i)%6
    if k>3:
        k=0
    tt[i]=k
    screen.vwrite(tc[i]*8,tp[k])
    screen.vfill(8192+tc[i]*8,8,ti[k])

def num(y,v):
    screen.vfill(y*32+184,160,0)
    screen.text(184,y,str(v),15)

def band(r0,r1):
    for r in range(r0,r1):
        a=r*256+XL
        screen.vfill(a,80,0)
        screen.vfill(8192+a,80,OC)

def tick(p):
    global zy,bs,sc,lv,iv
    for i in range(NT):
        a=tr[i]*256+tc[i]*8
        screen.vwrite(a,gp[gi[tc[i]-C0]])
        r=tr[i]+1
        if r>FR:
            feed(i)
        else:
            tr[i]=r
            a=a+256
            k=tt[i]
            screen.vwrite(a,tp[k])
            screen.vfill(8192+a,8,ti[k])
    for i in range(NE):
        q=0
        if eb[i]>0:
            eb[i]=eb[i]-1
            if eb[i]>0:
                sprite.put(4+i,ex[i],ey[i],8+(eb[i]&1)*3,4)
                continue
            ey[i]=FR*8
            q=1
        y=ey[i]+sp
        if y>FR*8:
            y=0
            ex[i]=XL+((ex[i]-XL+i*24+40)%XW)
        ey[i]=y
        x=ex[i]
        if p&1==0:
            x=x+hx[1+(p+i+i)%8]
            if x<XL:
                x=XL
            if x>XR:
                x=XR
            ex[i]=x
        if q:
            sprite.put(4+i,x,y,7,1)
        else:
            sprite.put(4+i,x,y)
    if zy>0:
        zy=zy-16
        if zy<8:
            zy=0
            sprite.hide(2)
        else:
            sprite.put(2,zx,zy)
            for i in range(NE):
                if eb[i]==0 and abs(ey[i]-zy)<8 and abs(ex[i]-zx)<8:
                    sc=sc+20
                    eb[i]=6
                    zy=0
                    sprite.hide(2)
                    break
    if bs>0:
        bs=bs-1
        if bs==0:
            sprite.hide(3)
        elif bs==1:
            sprite.put(3,bx,bg)
            c=(bx+4)//8
            r=(bg+4)//8
            for i in range(NT):
                if tc[i]==c and tr[i]==r and tt[i]>0 and tt[i]<3:
                    sc=sc+50
                    screen.vwrite(r*256+c*8,gp[gi[c-C0]])
                    feed(i)
        else:
            sprite.put(3,bx,bg+(bs-1)*8)
    if iv>0:
        iv=iv-1
    else:
        for i in range(NE):
            if eb[i]==0 and abs(ey[i]-py)<7 and abs(ex[i]-px)<7:
                eb[i]=6
                lv=lv-1
                iv=48
                break
    if iv&4:
        sprite.hide(0)
    else:
        sprite.put(0,px,py)
    sprite.put(1,px,py-SGH)

def start():
    global px,py,zy,bs,sc,lv,sp,iv
    art()
    px=120
    py=BOT
    zy=0
    bs=0
    sc=0
    lv=3
    sp=4
    iv=0
    screen.text(184,16,"SCORE",11)
    screen.text(184,40,"HI",11)
    screen.text(184,64,"SHIP",11)
    num(24,sc)
    num(48,hs)
    num(72,lv)
    for i in range(NT):
        tc[i]=C0+FC[i]
        tr[i]=i*3
        tt[i]=0
        screen.vwrite(tr[i]*256+tc[i]*8,TREE)
    for i in range(NE):
        eb[i]=0
        ex[i]=XL+(i*19)%XW
        ey[i]=i*28
        sprite.put(4+i,ex[i],ey[i],7,1)
    sprite.put(0,px,py,15,0)
    sprite.put(1,px,py-SGH,15,2)
    sprite.put(2,0,208,11,3)
    sprite.put(3,0,208,9,4)

def timed():
    global zx,zy,bx,bg,bs
    start()
    c=0
    t=time.tick()
    for p in range(60):
        if zy==0 and p&3==0:
            zx=px
            zy=py
        if bs==0 and p&7==4:
            bx=px
            bg=py-SGH
            bs=4
        tick(p)
        c=c+px+sc
        for i in range(NE):
            c=c+ex[i]+ey[i]
        for i in range(NT):
            c=c+tc[i]+tr[i]+tt[i]
    g=time.tick()-t
    if g<0:
        g=g+65536
    screen.mode(0)
    print("XPY MZEBI F="+str(g)+" C="+str(c))
    print("PRESS A KEY")
    key.flush()
    key.get()

def play():
    global px,py,zx,zy,bx,bg,bs,sp,hs
    start()
    n=0
    ls=0
    ll=lv
    while True:
        u=joy.stick(0)
        if u>0:
            x=px+hx[u]
            y=py+hy[u]
            if x<XL:
                x=XL
            if x>XR:
                x=XR
            if y<TOP:
                y=TOP
            if y>BOT:
                y=BOT
            px=x
            py=y
        if zy==0 and joy.trig(0):
            zx=px
            zy=py
            sound.play("T240L32V13O6CG")
        if bs==0 and key.pressed("M"):
            bx=px
            bg=py-SGH
            bs=4
            sound.play("T240L16V14O4GC")
        tick(n)
        n=n+1
        if sc!=ls:
            ls=sc
            sp=4+sc//400
            if sp>8:
                sp=8
            num(24,sc)
            sound.play("T255L64V13O2CO1C")
        if lv!=ll:
            ll=lv
            num(72,lv)
            sound.play("T200L16V15O2CO1CO1C")
        if lv<1:
            break
        if key.pressed("ESC"):
            return
    sprite.clear()
    if sc>hs:
        hs=sc
        num(48,hs)
    band(9,12)
    screen.text(92,80,"GAME OVER",9)
    sound.play("T100L8V15O4CO3GEC")
    time.sleep(90)
    key.flush()
    key.get()

def title():
    art()
    band(3,15)
    screen.text(52,32,"M Z E B I",15)
    screen.text(24,56,"A KEY FLIES T TIMES",11)
    screen.text(24,80,"TRIGGER ZAPS  M BOMBS",3)
    screen.text(52,104,"HI "+str(hs),9)

if sys.msx()<2:
    print("MZEBI WANTS AN MSX2")
else:
    title()
    while True:
        k=key.get()
        if k==chr(27):
            break
        if k=="t" or k=="T":
            timed()
        else:
            play()
        title()
    screen.mode(0)
