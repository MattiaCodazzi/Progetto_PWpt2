# Museo - Progetto PW25 (Ristrutturazione con Django + Bootstrap)

## Requisiti
- Python 3.10+
- (Opzionale) PostgreSQL

## Installazione (Windows)
1. Estrarre il progetto in una cartella.
2. Aprire il Prompt dei comandi nella cartella.
3. Eseguire: scripts\setup.bat

## Installazione (Linux/Mac)
1. Estrarre il progetto in una cartella.
2. Aprire il terminale nella cartella.
3. Eseguire: bash scripts/setup.sh

## Credenziali di accesso
- Se non hai creato un superuser, accedi alla home pubblica.
- Per l'area admin, crea un superuser durante l'installazione.

## Cambiare Database
- **SQLite (default)**: lascia `DB_URL` commentata in `.env`
- **Postgres**: scommenta `DB_URL` e inserisci le credenziali.

## Avvio
- Windows: `scripts\run.bat`
- Linux/Mac: `bash scripts/run.sh`

