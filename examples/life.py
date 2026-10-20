# LIFE.PY - Conway's Life

W = 32; H = 24; GE = 24; CE = 768

def box(k, c):
    x = (k % W) * 8
    y = (k // W) * 8
    screen.line(x, y, x + 7, y + 7, c * 14 + 1, "BF")

screen.mode(5)
screen.line(0, 0, 255, 191, 1, "BF")
a = [0] * CE
b = [0] * CE
for k in [368, 369, 399, 400, 432, 67, 100, 130, 131, 132]:
    a[k] = 1; box(k, 1)
tc = 0; cs = 0
for g in range(GE):
    t = time.tick()
    for y in range(H):
        p = y - 1
        if p < 0: p = H - 1
        q = y + 1
        if q == H: q = 0
        r = y * W
        u = p * W
        v = q * W
        for x in range(W):
            l = x - 1
            if l < 0: l = W - 1
            m = x + 1
            if m == W: m = 0
            n = a[u+l]+a[u+x]+a[u+m]+a[r+l]+a[r+m]+a[v+l]+a[v+x]+a[v+m]
            c = 0
            if n == 3 or (n == 2 and a[r+x] == 1): c = 1
            b[r+x] = c
    d = time.tick() - t
    if d < 0: d = d + 65536
    tc = tc + d
    for k in range(CE):
        if b[k] != a[k]: box(k, b[k])
    t = time.tick(); e = 0
    for k in range(CE):
        a[k] = b[k]
        e = e + b[k]
    d = time.tick() - t
    if d < 0: d = d + 65536
    tc = tc + d
    cs = cs + (g + 1) * e
screen.text(0, 196, "XPY F=" + str(tc) + " C=" + str(cs))
