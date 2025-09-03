# Manuale di Utilizzo – Museo (Django + Bootstrap)

## Introduzione
Nella seconda parte del progetto abbiamo ristrutturato il lavoro iniziale utilizzando **Python**, **Django** e **Bootstrap**.  
L’obiettivo principale è stato quello di risolvere le criticità emerse nella prima consegna, sia dal punto di vista **funzionale** che **grafico/estetico**.  

Il risultato è un gestionale che consente al personale museale di amministrare in modo semplice ed efficiente il database del museo, attraverso le operazioni CRUD (Create, Read, Update, Delete).  
Particolare attenzione è stata posta al [miglioramento dei punti deboli evidenziati nella valutazione del primo progetto](miglioramenti.md).

---
IMPORTANTE: consigliamo la visione del sito a schermo intero o quantomeno a 3/4 di schermo 
---

## Struttura del sito
- **Home** → pagina iniziale con panoramica generale.  
- **Opere** → ricerca, inserimento, modifica ed eliminazione delle opere.  
- **Autori** → gestione completa degli autori.  
- **Sale** → visualizzazione e gestione delle sale espositive.  
- **Temi** → gestione dei temi associabili alle sale.  

---

## Navigazione
- Menù principale sempre visibile in alto.  
- Le pagine sono collegate tra loro tramite link diretti, per un accesso rapido alle varie sezioni.  

---

## Funzionalità principali

### 0. Home
- **Benvenuto** → sezione introduttiva che illustra le funzionalità principali del sito e include una piccola vetrina grafica.  
- **Novità** → spazio dedicato agli aggiornamenti o alle nuove funzionalità aggiunte al sistema.  
- **Informazioni** → bacheca per comunicazioni utili al personale. Cliccando sul pulsante dedicato si possono leggere in dettaglio gli avvisi o gli articoli.  

### 1. Opere
- **Ricerca** → il form consente di filtrare le opere per: autore (nome e cognome), titolo, anno singolo o intervallo di anni, tipologia (quadro/scultura) e sala.  
- **Inserimento** → lo stesso form viene utilizzato anche per aggiungere nuove opere (senza considerare i parametri di ricerca come intervalli).  
   - Qualora venga inserito un autore non presente nel database, non sarà necessario crearlo precedentemente nella pagina degli autori: al click su *Inserisci* comparirà un messaggio *“Autore non presente, vuoi inserirlo?”* insieme a un form dedicato. Alla conferma, l’autore verrà inserito e contestualmente sarà salvata anche l’opera indicata in precedenza.  
- **Modifica** → cliccando su una riga della tabella delle opere, il form si compila automaticamente con i dati dell’opera selezionata, consentendo la modifica di tutti i parametri principali.  
- **Eliminazione** → è possibile selezionare una o più opere tramite la casella a sinistra di ciascuna riga. Il pulsante “Elimina selezionate”, posto sopra la tabella, consente la cancellazione, previa conferma.  

### 1.1 Dettaglio autori
Nella tabella delle opere e in quella degli autori, i nomi degli autori sono cliccabili. Il click reindirizza a una **pagina dinamica** dedicata, che mostra:  
1. Anagrafica dell’autore  
2. Panoramica dell’attività  
3. Elenco completo delle opere realizzate dall’autore  

### 1.2 Dettaglio sale
Nella tabella delle opere, i nomi delle sale sono cliccabili. Il click reindirizza a una **pagina dinamica** dedicata, che mostra:  
1. Numero di opere esposte  
2. Dettagli della sala (nome, superficie, tema)  
3. Elenco delle opere presenti in quella sala  

### 2. Autori
- **Ricerca** → filtro per nome e cognome, nazione (sigla es. IT, FR), date di nascita e morte, periodo e stato (vivente/deceduto).  
- **Inserimento** → come per le opere, il form di ricerca funge anche da modulo di inserimento.  
- **Modifica** → funzionamento analogo a quello delle opere.  
- **Eliminazione** → analoga alle opere, con la differenza che il messaggio di conferma scompare dopo pochi secondi, per evitare cancellazioni accidentali di autori (operazione considerata rara).  

### 3. Sale
- **Visualizzazione** → elenco delle sale con sistema di paginazione. Passando il mouse sopra una card vengono mostrate le informazioni principali (tema e superficie).  
- **Modifica** → cliccando su una card si apre un pop-up che permette di aggiornare nome, metratura e tema della sala.  
   - Se la casella del tema viene lasciata vuota o compilata con un valore non riconosciuto, il tema risulta “non definito” (è possibile assegnare ad ogni sala solo 1 dei 10 temi presenti nel museo).  
   - All’interno del pop-up viene mostrata anche un’anteprima con alcune opere esposte nella sala, per mantenere la finestra leggera e gestibile.  

### 4. Temi
- **Visualizzazione** → elenco dei temi con paginazione. Al passaggio del mouse su una card viene mostrata una breve descrizione; cliccando sulla card si apre un pop-up con il numero di opere relative al tema e la sala in cui sono esposte.  
- **Ricerca** → disponibile un form per cercare i temi per nome.  

---

## Messaggistica a schermo
- **Verde** → operazione completata con successo.  
- **Rosso** → errore (campi non validi o operazioni non consentite).  
- **Giallo** → messaggi di avviso (es. conferma eliminazione).  

I messaggi non sono permanenti: scompaiono automaticamente dopo alcuni secondi, per evitare confusione qualora l’utente torni sul gestionale dopo un intervallo di tempo.  

---

## Conclusione
Il sistema realizzato consente una gestione **semplice**, **intuitiva** ed **efficace** del museo.  
Tutte le operazioni principali sono supportate da form chiari e conferme visive, riducendo al minimo il rischio di errori e migliorando l’esperienza d’uso.  

