# XPOLY.PY - rotating triangle, square and cube (turbo R)

CX=128
CY=92
HW=56
PART=260

tx=[0,-40,40]
ty=[-46,30,30]
tz=[0,0,0]
te=[0,1,1,2,2,0]
sx=[-38,38,38,-38]
sy=[-38,-38,38,38]
sz=[0,0,0,0]
se=[0,1,1,2,2,3,3,0]
cx=[]
cy=[]
cz=[]
ce=[0,1,1,3,3,2,2,0,4,5,5,7,7,6,6,4,0,4,1,5,2,6,3,7]

pl=[]
sine=[]
qx=[0,0,0,0,0,0,0,0]
qy=[0,0,0,0,0,0,0,0]
ox=[128,128,128,128,128,128,128,128]
oy=[92,92,92,92,92,92,92,92]
sc=0
cp=1
r0=""
r1=""

def mk():
    for n in range(64):
        sine.append(31+int(31.5*math.sin(n*0.0981748)))
    pl.append(0)
    for n in range(13):
        a=n*0.48332
        pl.append((4+int(3*math.sin(a)))*64+(4+int(3*math.sin(a+2.0944)))*8
                  +4+int(3*math.sin(a+4.18879)))
    pl.append(0)
    pl.append(511)
    for n in range(8):
        cx.append(44-(n&1)*88)
        cy.append(26-((n>>1)&1)*52)
        cz.append(34-((n>>2)&1)*68)

def art():
    screen.color(15,14,14)
    screen.mode(5)
    for n in range(1,16):
        v=pl[n]
        screen.palette(n,v>>6,v>>3&7,v&7)

def el(t):
    g=time.tick()-t
    if g<0:
        g=g+65536
    return g

M=[0,0,0,0,0,0,0,0,180,0,0,0,CX,CY,150]

def turn(p,ax,ay,az):
    s=sine[p&63]-31
    c=sine[(p+16)&63]-31
    t=sine[(p>>1)&63]-31
    u=sine[((p>>1)+16)&63]-31
    M[1]=c*8
    M[3]=-s*8
    M[5]=-(t*s)>>2
    M[6]=u*8
    M[7]=-(t*c)>>2
    M[9]=u*s>>2
    M[10]=t*8
    M[11]=u*c>>2
    turbo.xform(ax,ay,az,M,qx,qy)

def wire(e,n,c,w):
    i=0
    while i<n:
        a=e[i]
        b=e[i+1]
        if w==1:
            screen.line(ox[a],oy[a],ox[b],oy[b],14)
        screen.line(qx[a],qy[a],qx[b],qy[b],c)
        i=i+2
    if w==1:
        for i in range(8):
            ox[i]=qx[i]
            oy[i]=qy[i]

def band(e,n,p):
    j=7
    while j>0:
        i=0
        while i<n:
            a=e[i]
            b=e[i+1]
            screen.line(CX+((qx[a]-CX)*j>>3),CY+((qy[a]-CY)*j>>3),
                        CX+((qx[b]-CX)*j>>3),CY+((qy[b]-CY)*j>>3),1+(j+p>>2)%13)
            i=i+2
        j=j-1

def tick(p):
    if sc==0:
        turn(p,tx,ty,tz)
        wire(te,6,9,1)
    elif sc==1:
        screen.line(CX-HW,CY-HW,CX+HW,CY+HW,14,"BF")
        turn(p,tx,ty,tz)
        band(te,6,p)
    elif sc==2:
        turn(p,sx,sy,sz)
        wire(se,8,5,1)
    elif sc==3:
        screen.line(CX-HW,CY-HW,CX+HW,CY+HW,14,"BF")
        turn(p,sx,sy,sz)
        band(se,8,p)
    elif sc==4:
        screen.line(CX-HW,CY-HW,CX+HW,CY+HW,14,"BF")
        turn(p,cx,cy,cz)
        wire(ce,24,11,0)
    else:
        screen.line(CX-HW,CY-HW,CX+HW,CY+HW,14,"BF")
        turn(p,cx,cy,cz)
        band(ce,24,p)

def show():
    global sc
    sc=4
    art()
    p=0
    while True:
        tick(p)
        p=p+1
        if p%PART==0:
            sc=sc+1
            if sc>5:
                sc=0
            art()
            for i in range(8):
                ox[i]=CX
                oy[i]=CY
        if key.pressed("ESC"):
            return

def timed():
    global cp,r0,r1,sc
    sc=4
    art()
    for Q in [0,2]:
        turbo.cpu(Q,True)
        cp=Q
        t=time.tick()
        for p in range(60):
            tick(p)
        g=el(t)
        t=time.tick()
        c=0
        for p in range(60):
            turn(p,cx,cy,cz)
            for i in range(8):
                c=c+qx[i]+qy[i]
        h=el(t)
        if Q==0:
            r0=" F"+str(g)+" C"+str(c)+" T"+str(h)
        else:
            r1=" F"+str(g)+" C"+str(c)+" T"+str(h)
    turbo.cpu(2,True)
    cp=1
    screen.mode(0)
    print("XPY XPOLY Q0"+r0)
    print("XPY XPOLY Q1"+r1)
    print("60 TICKS  HEAP "+str(sys.mem()[0]))
    print("THE TWO C MUST AGREE")
    print("PRESS A KEY")
    key.flush()
    key.get()

if sys.msx()<4:
    print("XPOLY WANTS A TURBO R")
else:
    mk()
    turbo.cpu(2,True)
    art()
    screen.text(56,52,"X P O L Y",15)
    screen.text(24,84,"A KEY - RUN IT",9)
    screen.text(24,100,"T     - TIME IT",9)
    screen.text(24,132,"WIRE, THEN SOLID, AND IT",7)
    screen.text(24,144,"TURNS ITSELF.  ESC LEAVES.",7)
    k=key.get()
    if k=="t" or k=="T":
        timed()
    else:
        show()
    turbo.cpu(0,True)
    screen.mode(0)
