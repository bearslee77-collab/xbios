# LIFE.PY (disk) - Conway's Life, board stored as bits

W = 32; H = 24; GE = 24

def box(k, c):
    x = (k % W) * 8
    y = (k // W) * 8
    screen.line(x, y, x + 7, y + 7, c * 14 + 1, "BF")

def unpack(s, y, t):
    w0 = s[y * 2]
    w1 = s[y * 2 + 1]
    for x in range(16):
        t[x] = (w0 >> x) & 1
        t[x + 16] = (w1 >> x) & 1

screen.mode(5)
screen.line(0, 0, 255, 191, 1, "BF")
a = [0] * (H * 2)
b = [0] * (H * 2)
for k in [368, 369, 399, 400, 432, 67, 100, 130, 131, 132]:
    x = k % W
    i = (k // W) * 2 + x // 16
    a[i] = a[i] | (1 << (x % 16))
    box(k, 1)

up = [0] * W; me = [0] * W; dn = [0] * W
tc = 0; cs = 0
for g in range(GE):
    t = time.tick(); e = 0
    unpack(a, H - 1, up)
    unpack(a, 0, me)
    for y in range(H):
        q = y + 1
        if q == H: q = 0
        if y > 0:
            r = up; up = me; me = dn; dn = r
        unpack(a, q, dn)
        w0 = 0; w1 = 0
        for x in range(W):
            l = x - 1
            if l < 0: l = W - 1
            m = x + 1
            if m == W: m = 0
            n = up[l]+up[x]+up[m]+me[l]+me[m]+dn[l]+dn[x]+dn[m]
            if n == 3 or (n == 2 and me[x] == 1):
                e = e + 1
                if x < 16: w0 = w0 | (1 << x)
                else: w1 = w1 | (1 << (x - 16))
        b[y * 2] = w0
        b[y * 2 + 1] = w1
    d = time.tick() - t
    if d < 0: d = d + 65536
    tc = tc + d
    for i in range(H * 2):
        c = a[i] ^ b[i]
        if c:
            k = (i // 2) * W + (i % 2) * 16
            for j in range(16):
                if (c >> j) & 1: box(k + j, (b[i] >> j) & 1)
    t = time.tick()
    for i in range(H * 2):
        a[i] = b[i]
    d = time.tick() - t
    if d < 0: d = d + 65536
    tc = tc + d
    cs = cs + (g + 1) * e
screen.text(0, 196, "XPY F=" + str(tc) + " C=" + str(cs))
