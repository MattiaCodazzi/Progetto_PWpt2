@echo off
REM Avvia lo script PowerShell bypassando la restrizione esecuzione
powershell -ExecutionPolicy Bypass -File "%~dp0setup.ps1"
pause

