# XPY

`xpybank.rom` — 128KB, ASCII16 메가롬. 빈 슬롯에 넣고 전원을 켜면 `>>>` 가 나옵니다.
RAM 64KB 가 필요합니다.

- 사용 가능한 메모리: 8749바이트 (디스크 ROM 이 있으면 5942바이트)
- 디스크 ROM(`../xdisk/xdisk.rom`)이 있으면 `fs.load("XMAZE.PY")` 로 디스크의 프로그램을 실행하고,
  `:save NAME` · `:load NAME` 으로 프로그램을 저장합니다.
- turbo R(RAM 256KB 이상)에서는 RAM 으로 복사해서 실행합니다.
