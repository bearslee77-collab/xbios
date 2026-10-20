# XPY 함수 목록

XPY는 MSX에서 돌아가는 파이썬입니다. 이 문서는 XPY에서 쓸 수 있는 형, 내장 함수, 모듈과 함수를 정리한 참고서입니다.

## 1. 사용 방법

- 모듈은 모두 내장되어 있어서 `import` 없이 이름으로 바로 씁니다. 예: `screen.pset(10, 20)`
- 좌표는 항상 왼쪽 위가 (0, 0)입니다.
- 인수를 생략할 수 있는 자리의 기본값은 `None`이며, 현재 설정을 그대로 쓴다는 뜻입니다. `screen.color(0)`은 전경색을 검정으로 바꾸고, `screen.color(None)`은 바꾸지 않습니다.
- 범위를 벗어난 인수는 `ValueError`, 형이 맞지 않으면 `TypeError`, 그 기계에서 지원하지 않는 기능은 `NotImplementedError`, 디스크 오류는 `OSError`, 메모리 부족은 `MemoryError`가 발생합니다. Ctrl-STOP은 `KeyboardInterrupt`가 됩니다.
- 세대 표기는 MSX1, MSX2, MSX2+, turbo R 입니다. 표기가 없는 함수는 모든 세대에서 동작합니다.
- 일부 이름은 실행 환경에 따라 들어 있지 않을 수 있습니다. 해당 항목에 따로 적었습니다.

## 2. 지원하는 형과 문법

### 형

| 형 | 설명 |
| --- | --- |
| `int` | 부호 있는 32비트 정수 (−2147483648 ~ 2147483647) |
| `float` | 단정도(32비트) 실수. 유효 숫자는 약 7자리입니다 |
| `bool` | `True`, `False` |
| `str` | MSX의 바이트열입니다. 유니코드가 아니므로 `len("가")`는 2입니다 |
| `None` | 값 없음 |
| `list` | 가변 배열 |
| `dict` | 사전 (넣은 순서를 유지합니다) |

튜플과 `bytes` 형은 없습니다. 여러 값을 돌려주는 함수는 리스트를 돌려줍니다. VRAM이나 메모리에서 읽은 바이트열은 `str`로 돌려줍니다.

### 문장과 연산자

- 문장: `if/elif/else`, `while`, `for/in`, `break`, `continue`, `pass`, `def`, `return`, `global`, `try/except/finally`, `raise`, `del`, `assert`
- 연산자: `+ - * / // % ** << >> & | ^ ~`, 비교 `== != < <= > >=`, 논리 `and or not`, `in`, `not in`
- `a, b = b, a` 같은 두 값의 교환 대입을 쓸 수 있습니다.
- `/` 는 실수 나눗셈, `//` 는 정수 나눗셈입니다. 0으로 나누면 `ZeroDivisionError`가 발생합니다.
- `class`, `yield`, `with`, `lambda`, `import`, 데코레이터는 지원하지 않습니다.
- f-문자열은 `{식}`과 `{식:서식}` 형태를 지원합니다. `!r`, `=`, 서식 안의 `{}` 중첩은 지원하지 않습니다. f-문자열과 `format()`이 들어 있지 않은 환경에서는 `NotImplementedError`가 발생합니다.

## 3. 내장 함수

| 함수 | 설명 |
| --- | --- |
| `print(*args, sep=" ", end="\n")` | 화면에 출력합니다. `sep`, `end`가 없는 환경도 있습니다 |
| `input(prompt="")` | 한 줄을 입력받아 `str`로 돌려줍니다 |
| `len(x)` | `str`, `list`, `dict`의 길이 |
| `range(stop)` / `range(start, stop[, step])` | `for` 문에서 쓰는 정수 범위 |
| `int(x)` / `int(s, base)` | 정수로 바꿉니다. `base`는 2~36이고 `s`는 문자열이어야 합니다 |
| `float(x)` | 실수로 바꿉니다 |
| `str(x)` | 문자열로 바꿉니다 |
| `bool(x)` | 참/거짓으로 바꿉니다 |
| `list(x)` | 리스트로 바꿉니다 |
| `chr(n)` / `ord(s)` | 바이트값과 글자 사이를 변환합니다 |
| `abs(n)` | 절댓값 |
| `min(...)` / `max(...)` | 최솟값 / 최댓값. 인수 여러 개 또는 리스트 하나 |
| `sum(list)` | 합계 |
| `hex(n)` / `bin(n)` | `"0x1f"`, `"0b11111"` 형태의 문자열 |
| `sorted(list)` | 정렬된 새 리스트 |
| `format(값)` / `format(값, 서식)` | 서식에 맞춘 문자열 |
| `exit()` | 프로그램을 끝내고 열린 파일을 닫습니다 |

### format 서식

`[[채움]정렬][부호][0][너비][.자리수][형]` 형태입니다.

- 정렬: `<`, `>`, `^`, `=` (`=`는 수에만 씁니다)
- 부호: `+`, `-`, 빈칸 (문자열에는 쓸 수 없습니다)
- 형: `d`, `s`, `f` 또는 생략. `f`의 기본 소수 자리는 6이고 반올림은 0.5에서 짝수 쪽으로 합니다.
- `x`, `o`, `e`, `g`, `%`와 천 단위 구분은 지원하지 않으며 `ValueError`가 발생합니다.

```python
print(f"SCORE{s:5}  HI-SC{h:5}")
print(format(3.14159, ".2f"))     # 3.14
```

### 문자열 메서드

| 메서드 | 설명 |
| --- | --- |
| `s.find(t)` | `t`가 처음 나오는 위치(0부터). 없으면 −1 |
| `s.rfind(t)` | 마지막으로 나오는 위치. 없으면 −1 |
| `s.index(t)` | `find`와 같고, 없으면 `ValueError` |
| `s.count(t)` | 겹치지 않게 센 횟수 |

### 리스트와 사전 메서드

| 메서드 | 설명 |
| --- | --- |
| `append(x)`, `insert(i, x)`, `extend(list)` | 항목을 더합니다 |
| `pop([i])`, `remove(x)`, `clear()` | 항목을 뺍니다 |
| `index(x)`, `count(x)` | 위치 찾기, 개수 세기 |
| `reverse()` | 순서를 뒤집습니다 |
| `d.get(k[, default])` | 사전에서 값을 꺼냅니다 |
| `d.update(other)` | 다른 사전을 합칩니다 |

### 파일 객체

`fs.open()`이 돌려주는 객체입니다.

| 메서드 | 설명 |
| --- | --- |
| `f.read([n])` | 최대 `n`바이트를 읽습니다. 생략하면 끝까지 읽습니다 |
| `f.readline()` | 한 줄을 읽습니다. 끝이면 `""` |
| `f.readlines()` | 모든 줄을 리스트로 읽습니다 |
| `f.write(s)` | 씁니다. 쓴 글자 수를 돌려줍니다 |
| `f.writelines(list)` | 문자열 리스트를 씁니다 |
| `f.seek(pos)` / `f.tell()` | 바이트 위치를 옮기기 / 알아내기 |
| `f.close()` | 닫습니다 |

`for line in f:`로 줄 단위 반복을 할 수 있습니다. 텍스트 모드에서는 줄바꿈이 변환됩니다(읽을 때 CRLF가 LF로, 쓸 때 LF가 CRLF로). 동시에 열 수 있는 파일은 3개입니다.

## 4. screen: 화면과 그리기

### 모드와 텍스트

| 함수 | 설명 |
| --- | --- |
| `screen.mode(n)` | 화면 모드를 바꿉니다. 0~8, 9(한글 화면). 모드 번호는 기종이 지원하는 범위입니다 |
| `screen.width(n)` | 텍스트 모드의 한 줄 글자 수 |
| `screen.cls()` | 화면을 지웁니다 |
| `screen.color(fg=None, bg=None, border=None)` | 전경색, 배경색, 테두리색 |
| `screen.key(on)` | 펑션키 표시줄을 켜거나 끕니다 |
| `screen.locate(x, y)` | 텍스트 커서 위치 |
| `screen.cursor(on)` | 커서를 보이거나 숨깁니다 |
| `screen.write(s)` | 글자를 그대로 출력합니다. 제어 문자도 그대로 전달됩니다 |
| `screen.scroll_lines()` | 현재 쓸 수 있는 줄 수 |
| `screen.text(x, y, s, c=None)` | 그래픽 화면의 (x, y)에 글자를 그립니다 |

### 점, 선, 도형

| 함수 | 설명 |
| --- | --- |
| `screen.pset(x, y, c=None)` | 점을 찍습니다. 화면 밖 좌표는 아무것도 그리지 않습니다 |
| `screen.preset(x, y)` | 배경색으로 점을 찍습니다 |
| `screen.point(x, y)` | 점의 색을 읽습니다. 화면 밖이면 −1 |
| `screen.line(x1, y1, x2, y2, c=None, mode="")` | 선을 그립니다. `mode`는 `""`(선), `"B"`(상자), `"BF"`(채운 상자). 화면을 벗어나는 끝점은 화면 안쪽으로 당겨집니다 |
| `screen.circle(x, y, r, c=None, aspect=None)` | 원을 그립니다. 호(각도 지정)는 없습니다 |
| `screen.paint(x, y, c=None, border=None)` | 경계색으로 둘러싸인 영역을 칠합니다. 시작점이 화면 밖이면 `ValueError` |
| `screen.draw(s)` | BASIC의 `DRAW` 명령 문자열을 실행합니다 |

텍스트 전용 모드에서 그리기 함수를 부르면 `ValueError`가 발생합니다. 색이 범위를 벗어나도 `ValueError`입니다. 점, 선, 원, 칠하기는 마지막 좌표를 그래픽 커서로 기억하고, `screen.draw`가 그 위치에서 이어서 그립니다. `screen.point`는 커서를 옮기지 않습니다.

`screen.draw` 문자열에서 쓸 수 있는 명령은 다음과 같습니다. 빈칸과 세미콜론은 무시되고 소문자도 됩니다. `X` 명령은 없습니다.

| 명령 | 뜻 |
| --- | --- |
| `U D L R E F G H` [n] | 8방향으로 n칸 이동하며 그립니다 |
| `M x,y` | 절대 좌표로 이동합니다. 첫 수에 부호가 있으면 상대 좌표입니다 |
| `B` / `N` | 다음 이동을 그리지 않음 / 그린 뒤 제자리로 돌아옴 |
| `C n` | 색 |
| `S n` | 배율 (4가 등배). `A n` 각도 0~3 (90도 단위) |

### VRAM과 VDP

| 함수 | 설명 |
| --- | --- |
| `screen.vpeek(addr)` / `screen.vpoke(addr, v)` | VRAM 1바이트 읽기/쓰기 |
| `screen.vread(addr, n)` | VRAM에서 `n`바이트를 `str`로 읽습니다 |
| `screen.vwrite(addr, data)` | `str`을 VRAM에 씁니다 |
| `screen.vfill(addr, n, v)` | VRAM을 같은 값으로 채웁니다 |
| `screen.vcopy(sx, sy, dx, dy, w, h, logop=None)` | 화면 안에서 사각형을 복사합니다. MSX2 이상 |
| `screen.vdp(reg, v)` | VDP 레지스터에 씁니다 |
| `screen.vdpstat(n=0)` | VDP 상태 레지스터를 읽습니다 |

MSX1에서 VRAM 주소는 0~0x3FFF이며 그 위는 `ValueError`입니다.

### MSX2 이상

| 함수 | 설명 |
| --- | --- |
| `screen.page(display, active=None)` | 표시할 페이지와 그리는 페이지를 정합니다. SCREEN 5~8에서 쓰며, 둘 다 `None`이면 `ValueError` |
| `screen.palette(n, r, g, b)` | 팔레트 `n`(0~15)을 정합니다. `r`, `g`, `b`는 0~7 |
| `screen.getpalette(n)` | `[r, g, b]` 리스트를 돌려줍니다 |
| `screen.resetpalette()` | 기본 팔레트로 되돌립니다 |

### MSX2+ 이상

| 함수 | 설명 |
| --- | --- |
| `screen.yjk(mode)` | YJK 모드를 켜고 끕니다. `None`(끔), 10, 11, 12. 먼저 `screen.mode(8)`이어야 합니다 |

### 한글 (SCREEN 9)

| 함수 | 설명 |
| --- | --- |
| `screen.hangul(on)` | 한글 입력을 켜고 끕니다 |
| `screen.hangul_state()` | 조합 중인 음절의 부호. 없으면 0 |

SCREEN 9에는 VRAM 128KB가 필요합니다. 한글 글꼴이 없는 화면에서는 `NotImplementedError`가 발생합니다.

### 회전·확대 (turbo R)

| 함수 | 설명 |
| --- | --- |
| `screen.rotozoom(tex, x, y, w, h, u, v, du, dv, duy=-dv, dvy=du)` | 16x16 텍스처(256바이트 `str`)를 창 `(x, y, w, h)`에 회전·확대하여 채웁니다 |

`u`, `v`는 창의 첫 점이 가리키는 텍스처 위치, `du`, `dv`는 가로 한 점마다, `duy`, `dvy`는 세로 한 줄마다 움직이는 양입니다. 모두 8.8 고정소수점이고 텍스처는 반복됩니다. 인수를 13개 주면 `tex`는 512바이트(텍스처 2장)이고 뒤의 `u2, v2, du2, dv2`가 둘째 텍스처의 값이며, 두 텍셀의 합이 점의 색이 됩니다. SCREEN 5, 7, 8에서만 동작합니다. 이 이름이 들어 있는 실행 환경에서만 쓸 수 있습니다.

## 5. sprite

| 함수 | 설명 |
| --- | --- |
| `sprite.size(pixels=8, magnify=False)` | 스프라이트 크기(8 또는 16)와 확대 여부 |
| `sprite.pattern(n, data)` | 패턴 `n`을 정합니다. `data`는 8바이트(8x8) 또는 32바이트(16x16)의 `str` |
| `sprite.put(n, x, y, color=None, pattern=None)` | 스프라이트 `n`(0~31)을 (x, y)에 표시합니다. y는 보이는 위치 그대로 씁니다 |
| `sprite.hide(n)` | 화면 밖으로 치웁니다 |
| `sprite.clear()` | 모든 스프라이트를 지웁니다. 패턴은 지우지 않습니다 |
| `sprite.pos(n)` | `[x, y]` |
| `sprite.collision()` | 충돌 깃발이 서 있으면 `True` |
| `sprite.collision_at()` | 충돌 위치 `[x, y]`, 충돌이 없으면 `None`. MSX2 이상 |
| `sprite.fifth()` | 한 줄 제한을 넘긴 스프라이트 번호, 없으면 `None` |

`sprite.size`는 인수를 생략하면 현재 값이 아니라 기본값(8, 확대 없음)이 됩니다. 번호가 범위를 벗어나면 `ValueError`입니다.

## 6. sound

### PSG 레지스터

| 함수 | 설명 |
| --- | --- |
| `sound.init()` | PSG를 초기 상태로 되돌립니다 |
| `sound.psg(reg, v)` | PSG 레지스터 `reg`(0~13)에 씁니다 |
| `sound.psgread(reg)` | PSG 레지스터를 읽습니다 |

### 음 하나

| 함수 | 설명 |
| --- | --- |
| `sound.tone(ch, period, volume=15)` | 채널 `ch`(0~2)에 주기 `period`(0~4095)로 소리를 냅니다 |
| `sound.note(ch, note, octave=4, volume=15)` | 음 이름(`"C"`, `"C#"`, … `"B"`) 또는 0~11로 소리를 냅니다 |
| `sound.volume(ch, v)` | 볼륨 0~15. 16이면 엔벨로프를 따릅니다 |
| `sound.noise(period, channels=0)` | 노이즈 주기(0~31)와 적용 채널(비트 0~2) |
| `sound.envelope(period, shape)` | 엔벨로프 주기(0~65535)와 모양(0~15) |
| `sound.mixer(tone=0b111, noise=0b000)` | 채널별 톤/노이즈 선택 |
| `sound.off(ch=None)` | 한 채널 또는 전체를 끕니다 |
| `sound.beep()` | 삐 소리 |

### MML 연주

| 함수 | 설명 |
| --- | --- |
| `sound.play(mml, ch=0)` | BASIC의 `PLAY`와 같은 MML 문자열을 연주합니다. 연주는 백그라운드로 진행됩니다 |
| `sound.playing(ch=None)` | 연주 중이면 `True` |
| `sound.stop(ch=None)` | 연주를 멈춥니다 |

MML 명령은 `A`~`G`(`#`, `+`, `-`), `N`, `R`, `O`(1~8), `L`(1~64), `T`(32~255), `V`(0~15), `S`(0~15), `M`(1~65535), 점(`.`)입니다. 범위를 벗어나면 `ValueError`입니다. 변수를 참조하는 `X변수$;`와 `=변수;`는 없으며, 문자열을 `+`로 이어 만드십시오. 한 번의 호출은 한 목소리입니다.

### FM 음원 (MSX-MUSIC)

| 함수 | 설명 |
| --- | --- |
| `sound.has(name)` | `"psg"`, `"fm"`, `"audio"` 중 해당 장치가 있는지. 다른 이름은 `ValueError` |
| `sound.fm(reg, v)` | YM2413 레지스터에 씁니다 |
| `sound.fm_note(ch, note, octave=4, inst=1, volume=15)` | FM 음 하나를 냅니다. `volume`은 15가 가장 큽니다 |

장치가 없으면 `sound.fm`, `sound.fm_note`는 `NotImplementedError`입니다. 모든 세대에서 같게 동작합니다.

## 7. key, joy, pad

### key

| 함수 | 설명 |
| --- | --- |
| `key.get()` | 키 하나를 기다려 글자로 돌려줍니다 |
| `key.inkey()` | 눌린 키가 있으면 글자, 없으면 `""` |
| `key.line(prompt="")` | 한 줄을 입력받습니다 |
| `key.wait()` | 아무 키나 누를 때까지 기다립니다 |
| `key.flush()` | 키 버퍼를 비웁니다 |
| `key.matrix(row)` | 키보드 행(0~10)의 상태. 눌린 키는 0 비트 |
| `key.pressed(name)` | `"SPACE"`, `"ESC"`, `"F1"` 같은 이름의 키가 눌려 있으면 `True` |
| `key.caps(on=None)` | CAPS 램프 상태를 돌려주며, 인수를 주면 바꿉니다 |
| `key.stop(on=None)` | Ctrl-STOP을 `KeyboardInterrupt`로 올릴지 정합니다. 기본값은 켜짐 |

### joy

| 함수 | 설명 |
| --- | --- |
| `joy.stick(n=0)` | 방향. 0은 커서키, 1~2는 조이스틱 포트. 반환값은 0(중립)~8 |
| `joy.trig(n=0)` | 버튼. 0은 스페이스, 1~4는 조이스틱 버튼. `bool` |
| `joy.dir(n=0)` | `[dx, dy]` 형태로 각각 −1, 0, 1 |

### pad

| 함수 | 설명 |
| --- | --- |
| `pad.get(n)` | 터치패드 등의 값을 읽습니다 (0~7은 터치패드, 8 이상은 번호 그대로 전달) |
| `pad.paddle(n)` | 패들 값 (n은 1~12) |
| `pad.mouse(port=1)` | `[dx, dy, buttons]`. 마우스가 없어도 값이 돌아오므로 마우스가 연결된 경우에만 의미가 있습니다 |

## 8. mem: 메모리, I/O, BIOS

| 함수 | 설명 |
| --- | --- |
| `mem.peek(addr)` / `mem.poke(addr, v)` | 1바이트 읽기/쓰기 |
| `mem.peek16(addr)` / `mem.poke16(addr, v)` | 16비트 읽기/쓰기 |
| `mem.read(addr, n)` | `n`바이트를 `str`로 읽습니다 |
| `mem.write(addr, data)` | `str`을 메모리에 씁니다 |
| `mem.copy(dst, src, n)` | 메모리 복사. 겹치는 구간은 앞에서부터 복사하므로 패턴 채우기에 쓸 수 있습니다 |
| `mem.inp(port)` / `mem.out(port, v)` | Z80 I/O 포트 읽기/쓰기 |
| `mem.bios(addr, a=0, b=0, c=0, d=0, e=0, h=0, l=0)` | 본체 BIOS 루틴을 부릅니다. 결과는 `{"a","b","c","d","e","h","l","f","cy"}` 사전입니다 |
| `mem.subrom(addr, ...)` | 같은 형식으로 SUB-ROM 루틴을 부릅니다 |
| `mem.calslt(slot, addr, ...)` | 지정한 슬롯의 루틴을 부릅니다 |
| `mem.usr(addr, arg=0)` | 기계어 루틴을 BASIC의 `USR`과 같은 규칙으로 부릅니다. 인수는 0~65535 정수 또는 255바이트 이하 `str`, 반환값은 부호 있는 정수 또는 `str` |
| `mem.slot(page)` | 해당 페이지의 현재 슬롯 |
| `mem.enaslt(slot, page)` | 페이지의 슬롯을 바꿉니다 |
| `mem.rdslt(slot, addr)` / `mem.wrslt(slot, addr, v)` | 지정 슬롯의 메모리 읽기/쓰기 |

### 매퍼 (MSX2 이상)

| 함수 | 설명 |
| --- | --- |
| `mem.segments()` | 세그먼트 수 |
| `mem.segment(page, seg=None)` | 페이지에 연결된 세그먼트를 읽거나 바꿉니다. 페이지 3은 쓸 수 없습니다 |
| `mem.alloc_segment()` / `mem.free_segment(n)` | 현재는 정의된 실패로 동작하며 사용할 수 없습니다 |

MSX1에서는 `NotImplementedError`입니다. 시스템 변수는 이름 대신 주소로 접근합니다. 예: `mem.peek16(0xFC9E)`.

## 9. fs: 디스크

파일 이름은 MSX-DOS의 8.3 형식이며, 긴 이름은 `ValueError`입니다. 없는 파일은 `FileNotFoundError`입니다.

| 함수 | 설명 |
| --- | --- |
| `fs.open(name, mode="r")` | 파일을 엽니다. 모드는 `"r"`, `"w"`, `"a"`, `"rb"`, `"wb"`, `"ab"`. 이진 모드도 `str`을 다룹니다 |
| `fs.exists(name)` | 파일이 있으면 `True` |
| `fs.files(pattern="*.*")` | 파일 이름 리스트 |
| `fs.dir(pattern="*.*")` | 파일 이름을 BASIC의 `FILES`처럼 한 줄에 셋씩 출력합니다. 이 이름이 들어 있는 실행 환경에서만 쓸 수 있습니다 |
| `fs.kill(name)` | 파일을 지웁니다 |
| `fs.rename(old, new)` | 이름을 바꿉니다 |
| `fs.size(name)` | 파일 크기(바이트) |
| `fs.drive(n=None)` | 현재 드라이브를 알려주며, 인수를 주면 바꿉니다 |
| `fs.free()` | 남은 용량(바이트) |
| `fs.load(name)` | `.PY` 파일을 읽어 실행합니다 |
| `fs.save(name)` | 현재 프로그램 텍스트를 파일로 저장합니다 |

## 10. time

| 함수 | 설명 |
| --- | --- |
| `time.tick()` | 프레임 카운터(JIFFY). 초가 아니라 프레임입니다 |
| `time.hz()` | 화면 주파수 (60 또는 50) |
| `time.sleep(frames)` | 프레임 수만큼 기다립니다 |
| `time.ms(n)` | `n`밀리초에 해당하는 프레임 수 |
| `time.clock()` | `[년, 월, 일, 시, 분, 초]`. MSX2 이상. 연도는 1980~2079입니다 |
| `time.setclock(y, mo, d, h, mi, s)` | 시계를 맞춥니다. MSX2 이상 |
| `time.hook(fn)` | 인터럽트마다 부를 함수를 등록합니다. `None`이면 해제합니다. 지원하지 않는 환경에서는 `NotImplementedError`가 발생합니다 |
| `time.counter()` | 16비트 자유 실행 계수기 값. turbo R 전용 |
| `time.counter_hz()` | 그 계수기의 초당 증가 수(255682) |

`time.counter()`는 약 256밀리초마다 한 바퀴를 돌므로 그보다 짧은 시간의 차이를 재는 데 씁니다.

## 11. turbo: turbo R 전용

turbo R이 아닌 기계에서는 `NotImplementedError`가 발생합니다.

| 함수 | 설명 |
| --- | --- |
| `turbo.cpu(mode, lamp=None)` | CPU 모드. 0은 Z80, 1은 R800(ROM), 2는 R800(DRAM). `lamp`를 주면 램프 상태도 지정합니다. 범위 밖은 `ValueError` |
| `turbo.get()` | 현재 CPU 모드(0, 1, 2) |
| `turbo.pcm_play(data, rate)` | PCM을 재생합니다. `data`는 `str`이고 `rate`는 0~3으로 속도는 15750/(rate+1) Hz입니다. 빈 문자열은 아무것도 하지 않습니다 |
| `turbo.pcm_rec(n, rate)` | 녹음. 이 기계에는 오디오 입력이 없으므로 항상 `NotImplementedError`입니다 |
| `turbo.xform(xs, ys, zs, m, sx, sy, sz=None)` | 3D 꼭짓점 변환(회전·이동·투영)을 R800 속도로 합니다 |
| `turbo.rayview(wx, wy, ncol, cw, wh, hs, ceil, floor)` | 1인칭 레이캐스터의 뷰를 만듭니다 |
| `turbo.raycast(view, map, w, x, y, dx, dy, depth=None)` | 뷰에 한 프레임을 그립니다 |

PCM 데이터는 런렝스 형식입니다. 0x80이 무음 표본이고, 0x00 다음 바이트가 무음 표본 수입니다.

`turbo.xform`은 `xs`, `ys`, `zs`(꼭짓점 좌표 리스트)를 변환해 결과를 `sx`, `sy`(`sz`)에 제자리로 씁니다. `m`은 15개 정수 리스트로 `tx m11 m12 m13 ty m21 m22 m23 tz m31 m32 m33 cx cy d` 순서이며, 행렬은 부호 있는 8.8 고정소수점이고 `d`가 0이면 원근 투영을 하지 않습니다. `sx`가 `xs`와 같은 리스트여도 됩니다.

`turbo.rayview`와 `turbo.raycast`는 SCREEN 5 또는 7에서 동작하는 레이캐스터입니다. `rayview`가 만든 뷰는 각 열이 지난번에 무엇을 그렸는지 기억하여 바뀐 부분만 다시 그리므로, 화면을 다시 그렸으면 뷰도 새로 만드십시오. `map`은 한 줄에 `w`칸인 `str`로, 칸의 아래 니블이 가로면의 색, 위 니블이 세로면의 색이며 0은 빈 칸입니다. `x`, `y`는 시점(8.8), `dx`, `dy`는 시선 방향입니다. `depth`에 리스트를 주면 열마다 거리가 채워집니다.

`turbo.xform`, `turbo.rayview`, `turbo.raycast`, `screen.rotozoom`은 이 이름이 들어 있는 실행 환경에서만 쓸 수 있습니다.

## 12. sys

| 함수 | 설명 |
| --- | --- |
| `sys.msx()` | 세대. 1은 MSX1, 2는 MSX2, 3은 MSX2+, 4는 turbo R |
| `sys.vram()` | VRAM 크기(KB) |
| `sys.ram()` | RAM 크기(KB) |
| `sys.hz()` | `time.hz()`와 같습니다 |
| `sys.keyboard()` | 키보드 종류 이름(`"jp"`, `"int"`, `"kr"` 등) |
| `sys.charset()` | 문자셋 이름 |
| `sys.slots()` | 존재하는 슬롯 번호의 리스트 |
| `sys.exit(code=0)` | DOS로 돌아갑니다 |
| `sys.reset()` | 기계를 다시 시작합니다 |
| `sys.argv()` | 명령줄 낱말 리스트. 프로그램 이름은 들어 있지 않습니다 |
| `sys.mem()` | `[남은 힙, 남은 스택]` (바이트) |

`sys.vram()`, `sys.ram()`은 XBIOS가 아닌 환경에서 `NotImplementedError`일 수 있습니다. `sys.argv()`는 명령줄이 없는 환경에서 `NotImplementedError`입니다.

## 13. random

| 함수 | 설명 |
| --- | --- |
| `random.random()` | 0.0 이상 1.0 미만의 실수 |
| `random.randint(a, b)` | `a` 이상 `b` 이하의 정수 (양 끝 포함). `a > b`이면 `ValueError` |
| `random.seed(n)` | 씨앗을 정합니다. 인수가 필요합니다 |

난수 수열은 MSX BASIC 의 `RND` 와 같습니다. `seed(n)` 은 `n` 의 유효숫자만 쓰므로 `seed(1)` 과 `seed(1000)` 은 같은 수열을 냅니다. 같은 수열을 다시 얻으려면 같은 값으로 `seed(n)` 을 부르십시오.

## 14. math

| 함수 | 설명 |
| --- | --- |
| `math.sqrt(x)` | 제곱근. 음수는 `ValueError` |
| `math.sin(x)`, `math.cos(x)`, `math.tan(x)` | 삼각함수 (라디안) |
| `math.atan(x)` | 아크탄젠트 |
| `math.log(x)` | 자연로그. 0 이하는 `ValueError` |
| `math.exp(x)` | 지수함수. 너무 큰 값은 `OverflowError` |
| `math.floor(x)`, `math.ceil(x)` | 내림, 올림 (`int`) |
| `math.fabs(x)` | 실수 절댓값 |
| `math.pi`, `math.e` | 상수 (괄호 없이 씁니다) |

`**` 연산자는 실수 지수를 받습니다. 밑이 음수이면 `ValueError`입니다. 실수는 단정도이므로 인수가 아주 크면 삼각함수의 정밀도가 떨어집니다.

## 15. 확장 칩 모듈

`v9`, `opl4`, `audio`, `scc`, `psg2`, `midi`, `hrtimer`, `sn`, `sfg`, `fac`은 XBIOS2 계열 BIOS에서 확장 칩을 다루는 모듈입니다. 칩이 확장 모듈을 지원하는 XPY에서만 쓸 수 있습니다. 칩이 없으면 `has()`가 `False`를 돌려주며, 없는 칩에 대한 호출은 `NotImplementedError`, 인수가 잘못되면 `ValueError`, 인수 개수가 틀리면 `TypeError`입니다. XBIOS2가 아닌 BIOS에서는 `has()`도 `NotImplementedError`입니다. 빈 `str` 데이터는 아무것도 하지 않습니다.

### v9: V9990 (GFX9000)

| 함수 | 설명 |
| --- | --- |
| `v9.has()` | 칩이 있으면 `True` |
| `v9.mode(screen, depth)` | 화면 모드. `screen` 0=P1, 1=P2, 2=B1, 3=B3, 4=B7, 5=B0, 6=B2, 7=B4. `depth` 0~3 (2, 4, 8, 16비트) |
| `v9.write(addr, data)` / `v9.read(addr, n)` | VRAM 쓰기/읽기 (`str`) |
| `v9.setreg(r, v)` / `v9.getreg(r)` | 레지스터 쓰기/읽기 |
| `v9.palette(first, n, data)` | 팔레트. 색마다 R, G, B(각 0~31) 3바이트 |
| `v9.cmd(block)` | 블리터 명령 블록(R#32~R#52의 21바이트)을 실행합니다 |
| `v9.fill(x, y, w, h, colour)` | 사각형 채우기. `colour`는 16비트 값이며 8비트 화면에서는 `c * 257` |
| `v9.copy(sx, sy, dx, dy, w, h)` | 사각형 복사 |
| `v9.put(x, y, w, h, data)` / `v9.get(x, y, w, h, n)` | 사각형에 바이트를 넣기/빼기 |
| `v9.scroll(layer, x, y)` | 스크롤 |
| `v9.sprite(n, y, pattern, x, attr)` | 스프라이트 (비트맵 화면에서는 커서) |
| `v9.irq(enable, line)` / `v9.ack()` | 인터럽트 설정/확인 |
| `v9.name(layer, x, y, n)` | 패턴 화면의 이름표 칸에 패턴 `n`(0~8191)을 지정합니다 |
| `v9.pattern(layer, n, data)` | 패턴 `n`의 모양을 정합니다. `data`는 32바이트 |

### opl4: OPL4 (MoonSound)

| 함수 | 설명 |
| --- | --- |
| `opl4.has()` / `opl4.init()` | 칩 확인 / 초기화 |
| `opl4.fm(reg, value, bank)` | FM 레지스터 쓰기 |
| `opl4.wave(reg, value)` / `opl4.getwave(reg)` | 웨이브 레지스터 쓰기/읽기 |
| `opl4.tone(ch, tone, fnum, octave, level, pan)` | 웨이브 음색을 울립니다 |
| `opl4.off(ch)` | 키오프 |
| `opl4.write(addr, data)` / `opl4.read(addr, n)` | 웨이브 메모리 쓰기/읽기 (RAM은 `0x200000`부터) |
| `opl4.header(k, data)` | 사용자 음색 384+`k`(`k`는 0~127)의 머리 12바이트를 웨이브 RAM에 씁니다 |

### audio: MSX-AUDIO (Y8950)

| 함수 | 설명 |
| --- | --- |
| `audio.has()` / `audio.init()` | 칩 확인 / 초기화 |
| `audio.reg(r, v)` / `audio.getreg(r)` | 레지스터 쓰기/읽기 |
| `audio.write(addr, data)` / `audio.read(addr, n)` | 샘플 RAM 쓰기/읽기 |
| `audio.play(start, stop, rate, volume, repeat)` / `audio.stop()` | ADPCM 샘플 재생/정지 |

### scc: SCC / SCC+

| 함수 | 설명 |
| --- | --- |
| `scc.has()` / `scc.slot()` | 칩이 있는지 / 슬롯 번호 (없으면 `NotImplementedError`) |
| `scc.write(slot, addr, data)` / `scc.read(slot, addr, n)` | 주소는 `0x98xx`(SCC) 또는 `0xB8xx`(SCC+), 1~256바이트 |

### psg2: 두 번째 PSG

| 함수 | 설명 |
| --- | --- |
| `psg2.has()` / `psg2.init()` | 칩 확인 / 초기화 |
| `psg2.reg(r, v)` / `psg2.getreg(r)` | 레지스터 쓰기/읽기 |

### midi: MSX-MIDI

| 함수 | 설명 |
| --- | --- |
| `midi.has()` / `midi.init()` | 인터페이스 확인 / 초기화 (31250 baud) |
| `midi.send(b)` | 바이트 하나를 보냅니다 |
| `midi.recv()` | 바이트 하나를 받습니다. 받을 것이 없으면 `ValueError`이므로 먼저 `midi.status() & 2`를 확인하십시오 |
| `midi.status()` | 상태 |

### hrtimer: 고해상도 타이머

| 함수 | 설명 |
| --- | --- |
| `hrtimer.has()` | 타이머가 있는지 |
| `hrtimer.get()` | 3,579,545Hz로 세는 31비트 계수 값. 약 10분에 한 바퀴 돕니다 |
| `hrtimer.reset()` | 0으로 되돌립니다 |

### sn: SN76489

| 함수 | 설명 |
| --- | --- |
| `sn.init()` / `sn.write(b)` | 초기화 / 바이트 쓰기. 칩을 찾을 수 없으므로 `has()`가 없고 오류도 나지 않습니다 |

### sfg: 야마하 SFG (YM2151)

| 함수 | 설명 |
| --- | --- |
| `sfg.has()` / `sfg.slot()` | 카트리지 확인 / 슬롯 번호 |
| `sfg.init(slot)` | 초기화 |
| `sfg.reg(slot, r, v)` / `sfg.status(slot)` | 레지스터 쓰기 / 상태 읽기 |
| `sfg.send(slot, b)` / `sfg.recv(slot)` | 카트리지의 MIDI 송수신 (`recv`는 `midi.recv`와 같습니다) |

### fac: FAC MIDI

| 함수 | 설명 |
| --- | --- |
| `fac.has()` / `fac.init()` | 인터페이스 확인 / 초기화 |
| `fac.send(b)` / `fac.recv()` / `fac.status()` | `midi`와 같은 형태입니다. 쉴 때 `status()`는 133입니다 |
