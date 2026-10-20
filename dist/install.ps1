# XBIOS 기계 구성을 이 PC 의 openMSX 와 blueMSX 에 등록합니다.
#   install.bat 을 실행하거나: powershell -ExecutionPolicy Bypass -File install.ps1 [blueMSX 폴더]
param([string]$BlueMsxDir = '')

$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
$done = 0

function Find-Exe([string]$name, [string[]]$dirs) {
    $found = @()
    foreach ($d in $dirs) {
        if ($d -and (Test-Path $d)) {
            $found += Get-ChildItem -Path $d -Filter $name -File -Recurse -Depth 3 -ErrorAction SilentlyContinue |
                      ForEach-Object { $_.DirectoryName }
        }
    }
    $found | Sort-Object -Unique
}

$roots = @($env:ProgramFiles, ${env:ProgramFiles(x86)}, $env:LOCALAPPDATA, $env:USERPROFILE,
           [Environment]::GetFolderPath('Desktop'), (Join-Path $env:USERPROFILE 'Downloads'))
foreach ($drv in Get-PSDrive -PSProvider FileSystem) {
    if ($drv.Root -and (Test-Path $drv.Root)) {
        foreach ($sub in 'Games', 'Emul', 'Emulators', 'MSX', 'Tools', 'openMSX', 'blueMSX') {
            $roots += Join-Path $drv.Root $sub
        }
    }
}

# ---- openMSX --------------------------------------------------------------
Write-Host ''
Write-Host '[openMSX]'
$omsx = @()
$cmd = Get-Command openmsx -ErrorAction SilentlyContinue
if ($cmd) { $omsx += Split-Path $cmd.Source }
$omsx += Find-Exe 'openmsx.exe' $roots
$omsx = $omsx | Sort-Object -Unique
$userShare = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'openMSX\share\machines'

if ($omsx -or (Test-Path (Split-Path (Split-Path $userShare)))) {
    foreach ($o in $omsx) { Write-Host "  찾음: $o" }
    New-Item -ItemType Directory -Force $userShare | Out-Null
    Copy-Item (Join-Path $here 'openmsx\*.xml') $userShare -Force
    Copy-Item (Join-Path $here 'openmsx\*.rom') $userShare -Force
    Write-Host "  등록: $userShare"
    Write-Host '  기계 이름: XBIOS_1_XPY, XBIOS_2_XPY_DISK, XBIOS_TR_XPY 등'
    $done++
} else {
    Write-Host '  openMSX 를 찾지 못했습니다.'
}

# ---- blueMSX --------------------------------------------------------------
Write-Host ''
Write-Host '[blueMSX]'
$bm = @()
if ($BlueMsxDir) { $bm += $BlueMsxDir }
foreach ($key in 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*',
                 'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*',
                 'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*') {
    Get-ItemProperty $key -ErrorAction SilentlyContinue |
        Where-Object { $_.DisplayName -like '*blueMSX*' -and $_.InstallLocation } |
        ForEach-Object { $bm += $_.InstallLocation.TrimEnd('\') }
}
$bm += Find-Exe 'blueMSX.exe' $roots
$bm = $bm | Where-Object { Test-Path (Join-Path $_ 'blueMSX.exe') } | Sort-Object -Unique

if ($bm) {
    foreach ($b in $bm) {
        $machines = Join-Path $b 'Machines'
        New-Item -ItemType Directory -Force $machines | Out-Null
        foreach ($m in Get-ChildItem (Join-Path $here 'bluemsx') -Directory) {
            Copy-Item $m.FullName $machines -Recurse -Force
        }
        Write-Host "  등록: $machines"
    }
    Write-Host '  기계 이름: XBIOS 1 XPY, XBIOS 2 XPY, XBIOS 2+ XPY'
    $done++
} else {
    Write-Host '  blueMSX 를 찾지 못했습니다. 폴더를 직접 지정하려면:'
    Write-Host '  install.bat "C:\blueMSX"'
}

Write-Host ''
if ($done) {
    Write-Host "예제 디스크: $(Join-Path $here 'examples.dsk')"
} else {
    Write-Host '등록한 곳이 없습니다.'
}
