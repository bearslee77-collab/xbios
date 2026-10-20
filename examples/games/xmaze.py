# XMAZE.PY - first-person maze (turbo R)

NC=64
CW=2
WX=64
WY=48
WH=96
HS=24576
SP=44
TG=2
TK=40

L1=[65535,32769,48621,34821,43765,41489,48861,32961,
    48863,33281,47869,35461,60085,33329,49135,65535]
L2=[65535,34849,43949,41509,48885,33413,64189,34945,
    43967,43137,44733,41125,44981,40965,49149,65535]
L3=[65535,40965,45045,34833,60375,35409,47965,34881,
    60383,35345,47861,41605,44733,41089,49087,65535]

ax=[8,1,1]
ay=[1,1,1]
aa=[8,0,16]
ex=[15,0,15]
ey=[14,13,13]

pl=[0,0,511,2,144,504,128,200,265,401,474,146,219,292,365,438]

DX=[256,255,251,245,237,226,213,198,181,162,142,121,98,74,50,25,
    0,-25,-50,-74,-98,-121,-142,-162,-181,-198,-213,-226,-237,-245,-251,-255,
    -256,-255,-251,-245,-237,-226,-213,-198,-181,-162,-142,-121,-98,-74,-50,-25,
    0,25,50,74,98,121,142,162,181,198,213,226,237,245,251,255]
DY=[0,25,50,74,98,121,142,162,181,198,213,226,237,245,251,255,
    256,255,251,245,237,226,213,198,181,162,142,121,98,74,50,25,
    0,-25,-50,-74,-98,-121,-142,-162,-181,-198,-213,-226,-237,-245,-251,-255,
    -256,-255,-251,-245,-237,-226,-213,-198,-181,-162,-142,-121,-98,-74,-50,-25]

fw=[0,1,1,0,-1,-1,-1,0,1]
tn=[0,0,1,1,1,0,-1,-1,-1]

m=L1
ms=[]
V=""
px=384
py=384
pa=0
lv=0
al=1
st=0
r0=""
r1=""

def mk():
    for i in range(3):
        L=[L1,L2,L3][i]
        s=""
        for r in range(16):
            for c in range(16):
                if L[r]>>c&1==0:
                    s=s+chr(0)
                elif c==ex[i] and r==ey[i]:
                    s=s+chr(85)
                else:
                    s=s+chr(175)
        ms.append(s)

def art():
    screen.color(2,1,1)
    screen.mode(5)
    for n in range(1,16):
        v=pl[n]
        screen.palette(n,v>>6,v>>3&7,v&7)

def el(t):
    g=time.tick()-t
    if g<0:
        g=g+65536
    return g

def view():
    turbo.raycast(V,ms[lv],16,px,py,DX[pa],DY[pa])

def frame():
    global V
    screen.line(WX-2,WY-2,WX+NC*CW+1,WY+WH+1,2,"B")
    V=turbo.rayview(WX,WY,NC,CW,WH,HS,3,4)
    view()

def mv(u,v):
    global px,py
    if m[py>>8]>>((px+u+u)>>8)&1==0:
        px=px+u
    if m[(py+v+v)>>8]>>(px>>8)&1==0:
        py=py+v

def load(n):
    global m,px,py,pa,lv
    lv=n
    if n==0:
        m=L1
    elif n==1:
        m=L2
    else:
        m=L3
    px=ax[n]*256+128
    py=ay[n]*256+128
    pa=aa[n]

def bot():
    global pa
    u=DX[pa]*SP>>8
    v=DY[pa]*SP>>8
    if m[(py+v+v+v)>>8]>>((px+u+u+u)>>8)&1:
        pa=(pa+TG)&63
    else:
        mv(u,v)

def demo():
    global r0,r1
    for Q in [0,2]:
        art()
        turbo.cpu(Q,True)
        load(0)
        frame()
        c=0
        t=time.tick()
        for f in range(TK):
            bot()
            view()
            c=c+px+py+pa
        g=el(t)
        if Q==0:
            r0=" F"+str(g)+" C"+str(c)
        else:
            r1=" F"+str(g)+" C"+str(c)
    turbo.cpu(2,True)
    screen.mode(0)
    print("XPY XMAZE Q0"+r0)
    print("XPY XMAZE Q1"+r1)
    print(str(TK)+" TICKS  HEAP "+str(sys.mem()[0]))
    print("THE TWO C MUST AGREE")
    print("PRESS A KEY")
    key.flush()
    key.get()

def title():
    art()
    screen.text(64,32,"X M A Z E",2)
    screen.text(24,64,"SPACE - PLAY",10)
    screen.text(24,80,"B     - DEMO AND TIME IT",10)
    screen.text(16,112,"CURSOR OR STICK TO WALK",14)
    screen.text(16,128,"FIND THE YELLOW DOOR",5)
    screen.text(16,144,"ESC TO QUIT",14)

bp=""
def mkbp():
    global bp
    for n in range(48):
        bp=bp+chr(250-n-n-n-n-n)

def play():
    global al,px,py,pa,st
    st=0
    al=1
    art()
    load(0)
    frame()
    while al==1:
        s=joy.stick(0)
        if s>0:
            u=fw[s]
            w=tn[s]
            if w!=0:
                pa=(pa+w*TG)&63
            if u!=0:
                a=DX[pa]*SP*u>>8
                b=DY[pa]*SP*u>>8
                ox=px
                oy=py
                mv(a,b)
                if px==ox and py==oy:
                    turbo.pcm_play(bp,3)
            st=st+1
            view()
            if abs(px-ex[lv]*256-128)+abs(py-ey[lv]*256-128)<300:
                if lv>=2:
                    al=0
                else:
                    load(lv+1)
                    frame()
        if key.pressed("ESC"):
            return
    art()
    screen.text(48,64,"THE WAY OUT",2)
    screen.text(24,88,"STEPS "+str(st),2)
    screen.text(24,104,"PRESS A KEY",10)
    key.flush()
    key.get()

if sys.msx()<4:
    print("XMAZE WANTS A TURBO R")
else:
    mk()
    mkbp()
    turbo.cpu(2,True)
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
    turbo.cpu(0,True)
    screen.mode(0)
