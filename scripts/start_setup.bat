@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0"
set "PS_EXE=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"

if not exist "%PS_EXE%" (
  echo [ERRORE] powershell.exe non trovato.
  echo Avvia manualmente: powershell -ExecutionPolicy Bypass -STA -File ".\setup_museo_gui.ps1"
  pause & exit /b 1
)

if not exist ".\setup_museo_gui.ps1" (
  echo [ERRORE] setup_museo_gui.ps1 non trovato nella stessa cartella.
  pause & exit /b 1
)

"%PS_EXE%" -NoProfile -ExecutionPolicy Bypass -STA -File ".\setup_museo_gui.ps1"
set "ERR=%ERRORLEVEL%"
if not "%ERR%"=="0" (
  echo. & echo [ERRORE] Script terminato con codice %ERR%. & pause
)
popd
exit /b %ERR%

