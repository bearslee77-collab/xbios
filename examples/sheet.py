# SHEET.PY - spreadsheet on the SCREEN 9 hangul screen (MSX2)

COLS = "ABCDEF"
NR = 15
W = 12
X0 = 4
Y0 = 2

cell = {}
cell["A1"] = "품목"
cell["B1"] = "수량"
cell["C1"] = "단가"
cell["D1"] = "금액"
cell["E1"] = "비율(%)"
cell["A2"] = "공책"
cell["B2"] = "5"
cell["C2"] = "300"
cell["A3"] = "연필"
cell["B3"] = "12"
cell["C3"] = "100"
cell["A4"] = "지우개"
cell["B4"] = "4"
cell["C4"] = "150"
cell["A5"] = "볼펜"
cell["B5"] = "6"
cell["C5"] = "250"
cell["A6"] = "자"
cell["B6"] = "2"
cell["C6"] = "500"
for r in range(2, 7):
    cell["D" + str(r)] = "=B" + str(r) + "*C" + str(r)
    cell["E" + str(r)] = "=D" + str(r) + "*100/D8"
cell["A8"] = "합계"
cell["D8"] = "=SUM(D2:D6)"
cell["A9"] = "평균"
cell["D9"] = "=D8/5"

memo = {}
busy = {}

def tonum(s):
    if "." in s:
        return float(s)
    return int(s)

def peek(st):
    s = st[0]
    while st[1] < len(s) and s[st[1]] == " ":
        st[1] += 1
    if st[1] < len(s):
        return s[st[1]]
    return ""

def expr(st):
    v = term(st)
    c = peek(st)
    while c == "+" or c == "-":
        st[1] += 1
        w = term(st)
        if c == "+":
            v = v + w
        else:
            v = v - w
        c = peek(st)
    return v

def term(st):
    v = fac(st)
    c = peek(st)
    while c == "*" or c == "/":
        st[1] += 1
        w = fac(st)
        if c == "*":
            v = v * w
        elif w == 0:
            raise ValueError
        elif v % w == 0:
            v = v // w
        else:
            v = v / w
        c = peek(st)
    return v

def word(st):
    s = st[0]
    a = st[1]
    while st[1] < len(s) and (s[st[1]] >= "A" and s[st[1]] <= "Z" or s[st[1]] >= "0" and s[st[1]] <= "9" or s[st[1]] == "."):
        st[1] += 1
    return s[a:st[1]]

def fac(st):
    c = peek(st)
    if c == "(":
        st[1] += 1
        v = expr(st)
        if peek(st) != ")":
            raise ValueError
        st[1] += 1
        return v
    if c == "-":
        st[1] += 1
        return -fac(st)
    w = word(st)
    if w == "":
        raise ValueError
    if w[0] >= "0" and w[0] <= "9":
        return tonum(w)
    if w == "SUM":
        if peek(st) != "(":
            raise ValueError
        st[1] += 1
        a = word(st)
        if peek(st) != ":":
            raise ValueError
        st[1] += 1
        b = word(st)
        if peek(st) != ")":
            raise ValueError
        st[1] += 1
        t = 0
        for ci in range(COLS.find(a[0]), COLS.find(b[0]) + 1):
            for r in range(int(a[1:]), int(b[1:]) + 1):
                t = t + value(COLS[ci] + str(r))
        return t
    return value(w)

def value(name):
    if name in memo:
        return memo[name]
    if busy.get(name, 0) == 1:
        raise ValueError
    s = cell.get(name, "")
    v = 0
    if s != "" and s[0] == "=":
        busy[name] = 1
        st = [s[1:], 0]
        v = expr(st)
        if peek(st) != "":
            raise ValueError
        busy[name] = 0
    elif s != "":
        try:
            v = tonum(s)
        except ValueError:
            v = 0
    memo[name] = v
    return v

def up(s):
    t = ""
    for c in s:
        if c >= "a" and c <= "z":
            c = chr(ord(c) - 32)
        t = t + c
    return t

def cut(s, n):
    i = 0
    while i < len(s):
        k = 1
        if ord(s[i]) >= 128:
            k = 2
        if i + k > n:
            break
        i += k
    return s[:i]

def shown(name):
    s = cell.get(name, "")
    if s == "":
        return ""
    if s[0] != "=":
        try:
            tonum(s)
        except ValueError:
            return cut(s, W - 2)
    try:
        v = value(name)
    except ValueError:
        busy.clear()
        return " " * (W - 7) + "#ERR"
    except ZeroDivisionError:
        busy.clear()
        return " " * (W - 7) + "#DIV0"
    if v != int(v):
        t = format(v, ".2f")
    else:
        t = str(int(v))
    return " " * (W - 2 - len(t)) + t

def draw(ci, r, on):
    name = COLS[ci] + str(r)
    t = shown(name)
    t = t + " " * (W - 2 - len(t))
    screen.locate(X0 + ci * W, Y0 + r)
    if on:
        screen.write("[" + t + "]")
    else:
        screen.write(" " + t + " ")

def status(ci, r):
    name = COLS[ci] + str(r)
    screen.locate(0, 0)
    s = " XPY 계산표    " + name + ": " + cell.get(name, "")
    screen.write(s + " " * (78 - len(s)))

def board(ci, r):
    memo.clear()
    for c in range(len(COLS)):
        for k in range(1, NR + 1):
            draw(c, k, c == ci and k == r)

screen.mode(9)
screen.cls()
screen.locate(0, Y0)
h = "    "
for c in COLS:
    h = h + "     " + c + "      "
print(h)
for k in range(1, NR + 1):
    screen.locate(0, Y0 + k)
    screen.write(" " * (3 - len(str(k))) + str(k))
screen.locate(0, Y0 + NR + 2)
screen.write(" 방향키: 이동   RETURN: 입력   DEL: 지움   ESC: 끝")
ci = 0
r = 1
board(ci, r)
status(ci, r)
while True:
    k = key.get()
    oc = ci
    orr = r
    if k == chr(27):
        break
    if k == chr(28) and ci < len(COLS) - 1:
        ci += 1
    if k == chr(29) and ci > 0:
        ci -= 1
    if k == chr(30) and r > 1:
        r -= 1
    if k == chr(31) and r < NR:
        r += 1
    if k == chr(13) or k == chr(127):
        name = COLS[ci] + str(r)
        if k == chr(13):
            screen.locate(0, Y0 + NR + 4)
            screen.write(" " * 78)
            screen.locate(0, Y0 + NR + 4)
            s = input(" " + name + " 에 넣을 값: ")
            screen.locate(0, Y0 + NR + 4)
            screen.write(" " * 78)
            if s != "" and s[0] == "=":
                s = up(s)
            if s != "":
                cell[name] = s
        else:
            cell[name] = ""
        board(ci, r)
    elif oc != ci or orr != r:
        draw(oc, orr, False)
        draw(ci, r, True)
    status(ci, r)
screen.mode(0)
