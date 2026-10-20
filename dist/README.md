# XBIOS 1.0

## 파일

| 파일 | 크기 | 내용 |
|---|---:|---|
| `xbios_1.rom` | 32768 | MSX1 본체 ROM. 실기용 ROM 파일 |
| `xbios_lo_0000.bin` · `xbios_hi_4000.bin` | 16384 | `xbios_1.rom` 을 반으로 나눈 것 (16KB 두 칩 기종용) |
| `xbios_2.rom` · `xbios_2_sub.rom` | 32768 · 16384 | MSX2 본체 · SUB-ROM |
| `xbios_2p.rom` · `xbios_2p_sub.rom` | 32768 · 16384 | MSX2+ 본체 · SUB-ROM |
| `xbios_tr.rom` · `xbios_tr_sub.rom` | 32768 · 16384 | turbo R 본체 · SUB-ROM |
| `xpy/xpybank.rom` | 131072 | XPY (ASCII16 메가롬) |
| `xdisk/xdisk.rom` | 16384 | 디스크 인터페이스 ROM (WD2793) |
| `examples.dsk` | 737280 | 예제 디스크 |
| `openmsx/` | | openMSX 기계 구성 12종 |
| `bluemsx/` | | blueMSX 기계 구성 3종 |
| `install.bat` · `install.ps1` | | 이 PC 의 openMSX · blueMSX 를 찾아 기계 구성을 등록 |
| `diag/` | | 진단용 ROM |
| `CHECKSUMS.txt` | | SHA-256 · CRC-32 · SUM16 |
| `verify.ps1` | | ROM 칩에서 읽어 낸 파일과 대조 |

MSX2 이후의 ROM 은 에뮬레이터에서만 시험했습니다.

## MSX1 실기에 넣기

- 칩: 27C256 (32KB, 28핀). `xbios_1.rom` 을 오프셋 0 부터 그대로 기록합니다.
- 기록한 뒤 다시 읽어 대조합니다: `powershell -File verify.ps1 readback.bin`
- 원래 ROM 의 핀 배치가 27C256 과 같은지 기종의 서비스 매뉴얼로 확인하십시오.
- 1번 핀(VPP)은 VCC 에 연결합니다.

```
   VPP  1 +--v--+ 28  VCC
   A12  2 |     | 27  A14
    A7  3 |     | 26  A13
    A6  4 |     | 25  A8
    A5  5 |     | 24  A9
    A4  6 |     | 23  A11
    A3  7 |     | 22  /OE
    A2  8 |     | 21  A10
    A1  9 |     | 20  /CE
    A0 10 |     | 19  D7
    D0 11 |     | 18  D6
    D1 12 |     | 17  D5
    D2 13 |     | 16  D4
   GND 14 +-----+ 15  D3
```

16KB 두 칩 기종: BIOS 자리에 `xbios_lo_0000.bin`, BASIC 자리에 `xbios_hi_4000.bin` 을 기록합니다.
디스크 드라이브가 내장된 기종은 hi 쪽도 필요합니다.

원래 ROM 은 보관해 두십시오. 다시 꽂으면 원래대로 돌아갑니다.

## 시작 화면

카트리지가 없으면 시작 화면에 RAM · VRAM · 화면 주파수 · 조이스틱 상태가 표시됩니다.
마지막 줄은 `NO CARTRIDGE` · `READY` · `STOPPED, CODE nn` 중 하나입니다.


## 문제가 있을 때

| 증상 | 확인할 것 |
|---|---|
| 화면이 안 나옴 | 칩 방향, 핀, 소켓 접촉, 1번 핀 배선 |
| 화면에 깨진 글자 | 주소선 배치. `verify.ps1` 로 대조 |
| `STOPPED, CODE` | 숫자를 적어 두십시오 |
| 카트리지를 못 찾음 | 슬롯 접점. 카트리지 이름과 기종을 알려 주십시오 |

검은 화면만 나오면 `diag/xbios_beacon.rom` 을 칩에 기록해 넣어 보십시오(`diag/README.md`).
