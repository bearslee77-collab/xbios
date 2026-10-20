# SUNGJUK.PY - grade sheet on the SCREEN 9 hangul screen (MSX2)

SUB = ["국어", "영어", "수학", "국사", "윤리", "물리", "화학", "교련"]
NAME = ["김민수", "이정희", "박성철", "최영미", "정대현", "강수진", "조현우", "윤미경", "장석진", "한지영"]
SC = []
SC.append([88, 92, 75, 90, 85, 70, 78, 90])
SC.append([95, 89, 82, 94, 92, 76, 85, 88])
SC.append([72, 65, 91, 70, 74, 88, 93, 95])
SC.append([91, 96, 68, 88, 90, 62, 70, 85])
SC.append([65, 58, 77, 72, 80, 81, 75, 92])
SC.append([84, 90, 88, 86, 89, 85, 87, 86])
SC.append([78, 74, 95, 80, 76, 96, 91, 90])
SC.append([93, 88, 79, 96, 95, 72, 80, 84])
SC.append([58, 62, 55, 66, 70, 59, 61, 94])
SC.append([87, 85, 90, 84, 88, 91, 89, 87])
N = len(NAME)
K = len(SUB)

def rj(s, n):
    s = str(s)
    return " " * (n - len(s)) + s

def lj(s, n):
    s = str(s)
    return s + " " * (n - len(s))

def dec(t, n):
    a = (t * 10 + n // 2) // n
    return str(a // 10) + "." + str(a % 10)

def word(t, n):
    a = t // n
    if a >= 90:
        return "수"
    if a >= 80:
        return "우"
    if a >= 70:
        return "미"
    if a >= 60:
        return "양"
    return "가"

tot = []
for r in SC:
    tot.append(sum(r))
rank = []
for t in tot:
    k = 1
    for u in tot:
        if u > t:
            k += 1
    rank.append(k)

def sheet():
    screen.cls()
    print("        1987학년도 2학기 기말고사 성적일람표        3학년 2반  담임 박영호")
    print()
    h = "번호 이름   "
    for s in SUB:
        h += rj(s, 5)
    print(h + "  총점   평균  석차 평어")
    print("-" * 76)
    for i in range(N):
        line = rj(i + 1, 3) + "  " + lj(NAME[i], 7)
        for v in SC[i]:
            line += rj(v, 5)
        line += rj(tot[i], 6) + rj(dec(tot[i], K), 7) + rj(rank[i], 5)
        print(line + "   " + word(tot[i], K))
    print("-" * 76)
    a = "     과목평균"
    b = "     최고점  "
    for j in range(K):
        t = 0
        m = 0
        for i in range(N):
            t += SC[i][j]
            m = max(m, SC[i][j])
        a += rj(dec(t, N), 5)
        b += rj(m, 5)
    print(a)
    print(b)
    print()
    print("  아무 키나 누르면 개인별 성적통지표를 봅니다.  ESC 는 끝")

def card(i):
    screen.cls()
    print("                        성 적 통 지 표")
    print()
    print("    1987학년도 2학기       3학년 2반 " + str(i + 1) + "번   " + NAME[i])
    print()
    print("    과목   점수  평어")
    print("    " + "-" * 60)
    for j in range(K):
        v = SC[i][j]
        print("    " + lj(SUB[j], 6) + rj(v, 5) + "   " + word(v, 1) + "   " + "#" * (v // 4))
    print("    " + "-" * 60)
    print("    총점 " + str(tot[i]) + "    평균 " + dec(tot[i], K) + "    석차 " + str(rank[i]) + " / " + str(N) + "    평어 " + word(tot[i], K))
    print()
    print("    아무 키나 누르면 다음 학생,  ESC 는 끝")

screen.mode(9)
sheet()
k = key.get()
i = 0
while k != chr(27):
    card(i)
    i = (i + 1) % N
    k = key.get()
screen.mode(0)
