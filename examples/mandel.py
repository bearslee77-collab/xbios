# MANDEL.PY - Mandelbrot set in fixed point

W = 128
H = 191
IT = 8
MID = 95

X0 = -8806
Y0 = -5130
DX = 96
DY = 54
FOUR = 16384

screen.mode(5)
screen.cls()

cs = 0
t0 = time.tick()

for py in range(MID + 1):
    cy = Y0 + py * DY
    m = H - 1 - py
    for px in range(W):
        cx = X0 + px * DX
        zx = 0
        zy = 0
        i = 0
        while i < IT:
            x2 = (zx * zx) >> 12
            y2 = (zy * zy) >> 12
            if x2 + y2 > FOUR:
                break
            zy = ((zx * zy) >> 11) + cy
            zx = x2 - y2 + cx
            i = i + 1
        cs = cs + i
        c = i + 1
        x = px + px
        screen.line(x, py, x + 1, py, c)
        screen.line(x, m, x + 1, m, c)

el = time.tick() - t0
if el < 0:
    el = el + 65536
ms = el * 1000 // time.hz()

screen.text(0, 0, "XPY F=" + str(el) + " MS=" + str(ms) + " C=" + str(cs))
