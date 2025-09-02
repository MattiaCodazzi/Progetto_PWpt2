# 🚨 Errori comuni e soluzioni – Progetto Museo

## 1) Errore: `py` non è riconosciuto come comando interno o esterno  
**Causa:** su alcune macchine Windows il comando rapido `py` non è installato.  

**Soluzioni:**  
- Usare il comando `python` al posto di `py`.  
- In alternativa, avviare il progetto specificando l’eseguibile completo di Python (es. `C:\Users\UTENTE\AppData\Local\Programs\Python\Python311\python.exe`).  
- Se manca Python → scaricare da [python.org](https://www.python.org/downloads/), installare la versione 3.x, e assicurarsi di spuntare “Add to PATH” durante l’installazione.  

---

## 2) Errore: `psql` non è riconosciuto  
**Causa:** PostgreSQL è installato ma il comando `psql` non è nel PATH di sistema.  

**Soluzioni:**  
- Aggiungere la cartella `bin` di PostgreSQL al PATH (esempio: `C:\Program Files\PostgreSQL\16\bin`).  
- Oppure modificare lo script inserendo il percorso completo, ad esempio:  
  ```powershell
  "C:\Program Files\PostgreSQL\16\bin\psql.exe"
  ```  
- Se PostgreSQL non è installato, scaricare da [postgresql.org](https://www.postgresql.org/download/).  

---

## 3) Errore: `Cartella progetto non trovata`  
**Causa:** il percorso scelto contiene spazi o è scritto male.  

**Soluzioni:**  
- Usare il pulsante **Sfoglia** nel wizard, evitando di scrivere il percorso a mano.  
- Verificare che dentro la cartella ci sia il file `manage.py`.  

---

## 4) Errore: `manage.py non trovato`  
**Causa:** è stata selezionata la cartella `scripts/` invece della root del progetto.  

**Soluzione:**  
- Selezionare la cartella principale del progetto, non la sottocartella `scripts/`.  

---

## 5) Errore: `Creazione superuser fallita`  
**Causa:** un superuser con lo stesso username esiste già.  

**Soluzioni:**  
- Ignorare l’errore: il superuser è già presente.  
- Oppure cancellare l’utente manualmente da PostgreSQL e rilanciare lo script.  

---

## 6) Errore: `psql: FATAL: password authentication failed`  
**Causa:** password di `postgres` o dell’utente `museo_user` sbagliata.  

**Soluzioni:**  
- Controllare di aver inserito la password corretta nel wizard.  
- In caso di dubbi, reimpostare la password con:  
  ```sql
  ALTER USER museo_user WITH PASSWORD 'nuova_password';
  ```  

---

## 7) Errore: `pip not found` o problemi di dipendenze  
**Causa:** `pip` non installato o non aggiornato.  

**Soluzioni:**  
- Aggiornare `pip` con:  
  ```powershell
  python -m ensurepip --upgrade
  python -m pip install --upgrade pip
  ```  
- Se manca un pacchetto, installarlo manualmente con:  
  ```powershell
  python -m pip install nome_pacchetto
  ```  

---
