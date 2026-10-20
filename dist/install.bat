@echo off
rem XBIOS 기계 구성을 openMSX 와 blueMSX 에 등록합니다.
chcp 65001 >nul
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" %*
echo.
pause
