# Imposta errore come stop
$ErrorActionPreference = "Stop"

Write-Host "=== Avvio setup progetto Museo ==="

# Vai nella cartella dove si trova lo script
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

# 1. Creazione ambiente virtuale
Write-Host "[1/9] Creazione ambiente virtuale..."
if (-Not (Test-Path ".venv")) { python -m venv .venv }
.\.venv\Scripts\Activate.ps1

# 2. Installazione requirements
Write-Host "[2/9] Installazione pacchetti..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Creazione utente e database
Write-Host "[3/9] Creazione utente e database in Postgres..."
try {
    psql -U postgres -c "CREATE USER museo_user WITH PASSWORD 'museo_pw';"
} catch { Write-Host "Utente museo_user già esistente." }
try {
    psql -U postgres -c "ALTER USER museo_user CREATEDB;"
} catch { }
try {
    psql -U postgres -c "CREATE DATABASE museo_db OWNER museo_user;"
} catch { Write-Host "Database museo_db già esistente." }

# 4. Import dump
Write-Host "[4/9] Importazione dump..."
psql -U museo_user -d museo_db -f dump.sql

# 5. Migrazioni Django
Write-Host "[5/9] Migrazioni Django..."
python manage.py migrate

# 6. Creazione superuser
Write-Host "[6/9] Creazione superuser..."
$env:DJANGO_SUPERUSER_USERNAME="admin"
$env:DJANGO_SUPERUSER_EMAIL="admin@example.com"
$env:DJANGO_SUPERUSER_PASSWORD="adminadmin"
try { python manage.py createsuperuser --noinput } catch { Write-Host "Superuser già esistente." }
Remove-Item Env:DJANGO_SUPERUSER_USERNAME,Env:DJANGO_SUPERUSER_EMAIL,Env:DJANGO_SUPERUSER_PASSWORD -ErrorAction SilentlyContinue

# 7. Avvio server
Write-Host "[7/9] Avvio server Django..."
python manage.py runserver 0.0.0.0:8000
