#!/bin/bash
# Avvia lo script PowerShell su Linux/macOS

# Rende eseguibile il file .ps1
chmod +x "$(dirname "$0")/setup.ps1"

# Esegue il file PowerShell bypassando la ExecutionPolicy
pwsh -ExecutionPolicy Bypass -File "$(dirname "$0")/setup.ps1"

