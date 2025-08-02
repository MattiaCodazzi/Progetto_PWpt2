# Museo Django – Starter Kit

Refactoring del Progetto 1 (Museo) – Percorso A-1, Python + Django 5.

## Setup rapido
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # configura DB_URL & SECRET_KEY
python manage.py migrate
python manage.py runserver
```

Struttura, modelli e template sono placeholder: personalizzali seguendo le Linee Guida Progetto #2.
