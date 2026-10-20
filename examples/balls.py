# BALLS.PY - 32 sprites bouncing (MSX2)

N=32;F=120
screen.mode(5)
sprite.size(8,True)
sprite.pattern(0,chr(60)+chr(126)+chr(255)+chr(255)+chr(255)+chr(255)+chr(126)+chr(60))
for n in range(N):
    sprite.put(n,0,0,n%15+1,0)
c=0
t=time.tick()
for f in range(F):
    a=f&511
    b=(f+f)&511
    d=f&255
    e=(f+f)&255
    o=0
    w=0
    for n in range(N):
        if n&1:
            p=(b+o)&511
        else:
            p=(a+o)&511
        if p>255: p=511-p
        if n&2:
            q=(e+w)&255
        else:
            q=(d+w)&255
        if q>127: q=255-q
        q=q+32
        c=c+p+q
        sprite.put(n,p,q)
        o=o+7
        w=w+11
g=time.tick()-t
if g<0: g=g+65536
screen.text(0,180,"XPY F="+str(g)+" C="+str(c))
