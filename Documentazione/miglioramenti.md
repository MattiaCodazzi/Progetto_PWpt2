# Tabella Critiche e Correzioni – Progetto Museo

In questa sezione vengono indicate le criticità emerse nella valutazione del primo progetto e le relative correzioni introdotte nel Progetto 2, con la motivazione delle scelte effettuate.

| Problemi progetto 1 (come da valutazione) | Correzioni nel Progetto 2 |
|--------------------------|---------------------------|
| **Generale** | |
| Header anonimo, mancava il nome dell’applicazione | header presente anche nella home |
| Navigazione in posizione diversa tra home e altre pagine (effetto fastidioso) | la navigazione è posizionata nello stesso punto per tutte le pagine, senza variazioni |
| Palette rosa in contrasto con grigio poco armonica | abbiamo optato per schiarire il rosa e marcare di più il grigio |
| Mancanza di coerenza tra pagine (es. stili diversi tra opere e autori) | la tabella e il form delle pagine opere e autori hanno lo stesso layout a parte per i parametri |
| Paginazione solo sequenziale, senza numeri di pagina | abbiamo reso la paginazione più flessibile, permettendo all'utente di saltare a pagina X oltre alla sequenza, inoltre la paginazione è uniforme in tutte le pagine |
| **Temi** | |
| Descrizione visibile solo al click, non al passaggio del mouse | abbiamo messo la descrizione al passaggio del mouse |
| Al click sul tema non si aprono le sale collegate | al click si apre il pop-up con la sala che presenta il tema e il numero di opere esposte |
| Mancano informazioni: quante sale collegate, quante opere esposte | informazioni presenti nel pop-up e nella pagina dinamica di ogni sala |
| Assente maschera di ricerca dei temi | ricerca implementata |
| Paginazione solo sequenziale, mancano numeri di pagina | come già indicato, migliorata la paginazione |
| Ordine dei temi non chiaro (non alfabetico, non cronologico) | temi ordinati in ordine alfabetico |
| **Sale** | |
| Mancanza di icone/foto rappresentative per ogni sala | abbiamo inserito un'immagine come sfondo per ogni card della sala |
| Nella maschera di modifica non è chiaro quale sala si sta modificando | viene indicato nel pop-up il nome della sala, inoltre è possibile modificarne il nome |
| Una volta assegnato un tema non è possibile rimuoverlo | implementata la possibilità, con indicazione “non definito” per assenza di tema |
| Pulsante “salva” poco visibile (sembra testo normale) | aumentata la visibilità del tasto, ora denominato “Salva modifiche” |
| Tema mostrato col codice invece che col nome | il tema viene mostrato con il suo nome (es. Impressionismo) |
| Mancano link al tema o ad altre sale con lo stesso tema | tutte le informazioni di ogni sala si trovano nelle pagine dinamiche |
| Mancano filtri per selezionare sale di un tema | scelta di non implementare per semplicità e user-friendliness (solo 10 sale, non ampliabili) |
| Mancano informazioni sul numero di opere esposte nella sala | tutte le informazioni si trovano nelle pagine dinamiche di ogni sala |
| **Autori** | |
| La pagina si apre vuota, non mostra subito tutti gli autori | ora la pagina si apre mostrando tutti gli autori |
| Layout allineato a sinistra, incoerente con altre pagine centrate | layout centrato come le altre pagine |
| Uso tendine per nome/cognome → ricerca poco pratica, impossibile ricerca parziale | implementata ricerca parziale (partial match, LIKE) |
| Mancano filtri: vivi/morti, anno nascita/morte, range di date | aggiunti questi filtri |
| Mancano funzionalità di ordinamento dei dati | autori ordinati alfabeticamente per cognome |
| Non viene mostrato il numero di autori trovati | numero mostrato dopo ogni ricerca vicino a “risultati” |
| Mancanza di paginazione (tutti in una pagina unica) | paginazione uniforme e non solo sequenziale |
| Colonne con nomi poco chiari (es. “tipo” per stato) | colonna rinominata in “Stato” (vivo/morto) |
| Date mostrate in formato YYYY-MM-DD (poco leggibile per utenti) | ora mostrate come DD-MM-YYYY |
| Mancano informazioni: quante opere ha un autore, con relativo link | aggiunte queste informazioni tramite pagine dinamiche |
| Maschera di modifica sempre visibile, occupa spazio → meglio popup | maschera di modifica ora compare solo alla selezione di un autore |
| Validazioni mancanti (es. data morte < data nascita possibile) | aggiunti controlli sulle date |
| Messaggi di errore con alert del browser (non ammessi) | eliminati alert browser, sostituiti con messaggi personalizzati |
| **Opere** | |
| Stile pagina diverso da autori (incoerenza grafica) | mantenuto stesso stile, variando solo i parametri specifici |
| CRUD gestito con 4 pagine/tasti distinti (ridondante) | ora tutto il CRUD è gestito in un’unica pagina |
| Selezione tipo con tendina invece di radio button | sostituita tendina con radio button |
| Autore selezionato da tendina invece che campo di testo con ricerca parziale | implementata ricerca parziale anche per autore |
| Mancano filtri per anno di realizzazione/acquisto e range di anni | filtri aggiunti |
| Dati non linkati (clic autore o sala non porta a scheda) | dati ora linkati |
| Numeri non allineati a destra | numeri allineati a destra |
| Opere non esposte mostrate come “NULL” | ora indicato “non esposta” |
| Inserimento: anno minimo 1000 poco sensato | fascia ampliata da 0 a 2025 |
| Inserimento: autore e tipo con tendine (scelta poco pratica) | sostituiti con input più funzionali |
| Inserimento: quadri decorativi senza funzione, incoerenti | rimossi, aggiunta vetrina nella home |
| Modifica: controllo anni non ben posizionato, messaggi incoerenti con altre pagine | messaggi posizionati sotto i form; messaggio conferma eliminazione accanto al pulsante “Elimina selezionate” |
| Eliminazione: conferma con alert del browser | eliminati alert browser |
| Eliminazione: messaggi persistenti, rischio confusione | implementati messaggi non persistenti (5 secondi) |