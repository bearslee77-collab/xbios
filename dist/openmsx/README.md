# openMSX 기계 구성

| 세대 | XPY | XPY + 디스크 | XBIOS 만 |
|---|---|---|---|
| MSX1 | `XBIOS_1_XPY` | `XBIOS_1_XPY_DISK` | `XBIOS_1` |
| MSX2 | `XBIOS_2_XPY` | `XBIOS_2_XPY_DISK` | `XBIOS_2` |
| MSX2+ | `XBIOS_2P_XPY` | `XBIOS_2P_XPY_DISK` | `XBIOS_2P` |
| turbo R | `XBIOS_TR_XPY` | `XBIOS_TR_XPY_DISK` | `XBIOS_TR` |

## 설치

1. 이 폴더의 파일 전부(`.xml` 과 `.rom`)를 openMSX 의 `share\machines\` 에 복사합니다.
   Windows 에서는 보통 `%USERPROFILE%\Documents\openMSX\share\machines\` 입니다.
2. 기계 목록에서 고르거나 명령줄에서 실행합니다.

```
openmsx -machine XBIOS_TR_XPY
openmsx -machine XBIOS_TR_XPY_DISK -diska examples.dsk
```

- `_XPY` 는 켜면 `>>>` 가 나옵니다.
- `_XPY_DISK` 는 디스크 드라이브가 있고, `fs.load("이름.PY")` 로 디스크의 프로그램을 실행합니다.
- 카트리지를 꽂으면 카트리지가 먼저 실행됩니다.
- turbo R 기계의 RAM 은 256KB 입니다.
