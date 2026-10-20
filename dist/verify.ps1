# ROM 칩에서 읽어 낸 파일이 이 배포판과 같은지 본다.
#
#   powershell -File verify.ps1 readback.bin
#
# 프로그래머가 읽어 낸 파일을 그대로 주면 된다. 크기가 32768 이면 통짜 판과,
# 16384 이면 lo/hi 두 판 각각과 대 본다.

param([Parameter(Mandatory)][string]$File)

$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot

if (-not (Test-Path $File)) { throw "$File 이 없습니다" }
$got = [System.IO.File]::ReadAllBytes($File)
$hash = (Get-FileHash $File -Algorithm SHA256).Hash.ToLower()
$sum16 = 0; foreach ($b in $got) { $sum16 += $b }
$sum16 = $sum16 -band 0xFFFF

Write-Host ("읽은 파일  {0}" -f $File)
Write-Host ("  크기     {0}" -f $got.Length)
Write-Host ("  SHA-256  {0}" -f $hash)
Write-Host ("  SUM16    {0:X4}" -f $sum16)

# 같은 크기의 파일이 여럿이라 전부 대 본다.
$cands = @()
switch ($got.Length) {
    32768 { $cands = @('xbios_1.rom', 'xbios_2.rom', 'xbios_2p.rom', 'xbios_tr.rom') }
    16384 { $cands = @('xbios_lo_0000.bin', 'xbios_hi_4000.bin',
                       'xbios_2_sub.rom', 'xbios_2p_sub.rom', 'xbios_tr_sub.rom') }
    default {
        Write-Host ""
        Write-Host "크기가 32768 도 16384 도 아닙니다. 프로그래머의 칩 종류 설정을 볼 것." -ForegroundColor Yellow
        exit 2
    }
}

# 안 맞으면 제일 가까운 것 하나만 보여 준다.
$best = $null
foreach ($c in $cands) {
    $p = Join-Path $here $c
    if (-not (Test-Path $p)) { continue }
    $want = [System.IO.File]::ReadAllBytes($p)
    $n = 0
    $first = @()
    for ($i = 0; $i -lt $want.Length; $i++) {
        if ($got[$i] -ne $want[$i]) {
            $n++
            if ($first.Count -lt 8) {
                $first += ('${0:X4}: 있어야 할 ${1:X2}, 읽힌 ${2:X2}' -f $i, $want[$i], $got[$i])
            }
        }
    }
    if ($n -eq 0) {
        Write-Host ""
        Write-Host ("일치: {0} 과 바이트가 같습니다." -f $c) -ForegroundColor Green
        exit 0
    }
    if ($null -eq $best -or $n -lt $best.n) { $best = @{ c = $c; n = $n; first = $first } }
}

Write-Host ""
if ($null -eq $best) {
    Write-Host "댈 파일이 이 폴더에 없습니다." -ForegroundColor Red
    exit 2
}
Write-Host "어느 것과도 안 맞습니다." -ForegroundColor Red
Write-Host ("제일 가까운 것은 {0} 이고 {1}바이트 다릅니다. 앞 {2}개:" -f
    $best.c, $best.n, $best.first.Count) -ForegroundColor Yellow
$best.first | ForEach-Object { Write-Host ("  " + $_) }
Write-Host ""
Write-Host "한 비트씩만 틀리면 기록 실패나 접촉 불량, 통째로 다르면 주소선 배치를 볼 것."
exit 1
