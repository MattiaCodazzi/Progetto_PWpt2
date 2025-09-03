# 🚨 Errori comuni e guida user friendly– Progetto Museo (Django + PostgreSQL)

Questa guida spiega, passo‑passo, come risolvere i problemi più frequenti durante l’installazione su Windows:
- `py` / `python` non riconosciuto
- `psql` non riconosciuto

---

## 🔎 Controllo iniziale
Apri **PowerShell** o **Prompt dei comandi** e digita:
```powershell
py --version
python --version
psql --version
```
- Se i comandi funzionano → ok.  
- Se compare “*is not recognized*” → va aggiunto al **PATH**.

---

## ⚙️ Aggiungere Python (`py` o `python`) al PATH

### Caso A – Python non installato
1. Scaricare Python da [python.org](https://www.python.org/downloads/).  
2. Avviare l’installazione.  
3. **Selezionare l’opzione “Add python.exe to PATH”**.  
4. Riavviare PowerShell e verificare:
   ```powershell
   py --version
   python --version
   ```

### Caso B – Python già installato ma non nel PATH
1. Trovare la cartella che contiene `python.exe`, ad esempio:  
   - `C:\Users\NOME\AppData\Local\Programs\Python\Python312\`  
   - `C:\Program Files\Python312\`  
2. Copiare il percorso.  
3. Premere **Start →** cercare: **Modifica le variabili di ambiente relative al sistema**.  
4. Cliccare su **Variabili d’ambiente…**.  
5. In **Variabili di sistema** o **variabili dell'utente**, selezionare `Path` → **Modifica**.  
6. Cliccare su **Nuovo** e incollare il percorso copiato.  
7. Salvare con **OK**.  
8. Verificare in PowerShell:
   ```powershell
   python --version
   py --version
   ```

---

## ⚙️ Aggiungere PostgreSQL (`psql`) al PATH

1. Individuare la cartella `bin` di PostgreSQL, di solito:  
   - `C:\Program Files\PostgreSQL\16\bin`  
2. Copiare il percorso.  
3. Premere **Start →** cercare: **Modifica le variabili di ambiente relative al sistema**.    
4. Cliccare su **Variabili d’ambiente…**.  
5. In **Variabili di sistema** o **variabili dell'utente**, selezionare `Path` → **Modifica**.
6. Cliccare su **Nuovo** e incollare il percorso copiato.  
7. Salvare con **OK**.  
8. Verificare in PowerShell:
   ```powershell
   psql --version
   ```

---

## ✅ Checklist finale
- [ ] `py --version` oppure `python --version` funziona  
- [ ] `psql --version` funziona  

Se entrambi i test passano, lo script di installazione funziona correttamente.

---


---

## 🔐 Password PostgreSQL dimenticata (`postgres`)

**Importante:** la password dell’utente `postgres` **non può essere recuperata o visualizzata** perché è salvata in forma criptata.  
Se non la ricordi, puoi solo **reimpostarla con una nuova password**.

### Metodo 1 – Reimpostare con `pg_hba.conf`
1. Vai nella cartella dati di PostgreSQL, di solito:  
   `C:\Program Files\PostgreSQL\16\data\`  
2. Apri il file `pg_hba.conf` con un editor di testo.  
3. Trova la riga per l’host locale e sostituisci l’ultima colonna con `trust`:  
   ```
   host    all    all    127.0.0.1/32    trust
   ```  
4. Salva il file e riavvia il servizio PostgreSQL (da “Servizi” di Windows).  
5. Apri PowerShell ed entra senza password:  
   ```powershell
   psql -U postgres -h 127.0.0.1
   ```  
6. Cambia la password:  
   ```sql
   ALTER USER postgres WITH PASSWORD 'NuovaPasswordSicura';
   ```  
7. Ripristina `pg_hba.conf` rimettendo `md5` o `scram-sha-256` al posto di `trust`.  
8. Riavvia di nuovo PostgreSQL.  
9. Prova il login:  
   ```powershell
   psql -U postgres -h 127.0.0.1 -W
   ```  

### Metodo 2 – Se hai un altro superuser valido
1. Accedi con quell’utente (via `psql` o pgAdmin).  
2. Esegui:  
   ```sql
   ALTER USER postgres WITH PASSWORD 'NuovaPasswordSicura';
   ```  

---

✅ Dopo il reset, inserisci la nuova password nel wizard.  
Le credenziali del file `.env` (utente `museo_user`) **non vanno toccate**: servono solo all’applicazione.  

---

## Errore: `Cartella progetto non trovata`  
**Causa:** il percorso scelto contiene spazi o è scritto male.  

**Soluzioni:**  
- Usare il pulsante **Sfoglia** nel wizard, evitando di scrivere il percorso a mano.  
- Verificare che dentro la cartella ci sia il file `manage.py`.  

---

## Errore: `manage.py non trovato`  
**Causa:** è stata selezionata la cartella `scripts/` invece della root del progetto.  

**Soluzione:**  
- Selezionare la cartella principale del progetto, non la sottocartella `scripts/`.  

---

## Errore: `Creazione superuser fallita`  
**Causa:** un superuser con lo stesso username esiste già.  

**Soluzioni:**  
- Ignorare l’errore: il superuser è già presente.  
- Oppure cancellare l’utente manualmente da PostgreSQL e rilanciare lo script.  

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
