# Schede di Specifica dei Casi d'Uso Principali

Questo documento dettaglia i flussi di interazione per i casi d'uso più significativi del sistema.

---

### Scheda di Specifica: UC-P02

| **Nome del Caso d'Uso** | **UC-P02: Inserimento Dati Glicemici** |
| :--- | :--- |
| **Attore Principale** | Paziente |
| **Descrizione** | [cite_start]Il paziente, dopo essersi autenticato, memorizza le rilevazioni giornaliere di glicemia. |
| **Precondizioni** | [cite_start]L'attore "Paziente" deve essere autenticato e aver effettuato l'accesso al sistema. |
| **Postcondizioni** | La nuova misurazione di glicemia è salvata nel sistema e associata al profilo del paziente. [cite_start]Se il valore supera le soglie, il sistema avvia la procedura di alert per il medico. |

#### Flusso Principale (Scenario di Successo)
1.  Il paziente seleziona l'opzione per inserire una nuova misurazione di glicemia.
2.  Il sistema presenta un'interfaccia per l'inserimento dati.
3.  Il paziente inserisce il valore di glicemia (in mg/dL).
4.  Il paziente specifica il momento della misurazione (es. "prima di colazione", "dopo pranzo").
5.  Il paziente conferma l'inserimento.
6.  Il sistema valida che il valore inserito sia numerico e plausibile.
7.  Il sistema salva la misurazione, associandola al paziente con data e ora correnti.
8.  [cite_start]Il sistema verifica se il valore rientra nei livelli di normalità (tra 80 e 130 mg/dL prima dei pasti, non superiore a 180 mg/dL due ore dopo i pasti).
9.  Il sistema notifica al paziente che il dato è stato salvato con successo.

#### Flussi Alternativi ed Eccezioni
* **Dati non validi**: Se il paziente inserisce un valore non numerico nel campo della glicemia, il sistema mostra un messaggio di errore e richiede di inserire un numero valido prima di procedere.

---

### Scheda di Specifica: UC-M02

| **Nome del Caso d'Uso** | **UC-M02: Gestione Terapia** |
| :--- | :--- |
| **Attore Principale** | Medico |
| **Descrizione** | [cite_start]Il medico specifica, aggiunge o modifica la terapia che un paziente deve seguire, a seconda dell'evoluzione del suo stato. |
| **Precondizioni** | [cite_start]L'attore "Medico" deve essere autenticato e aver selezionato un paziente dalla lista dei pazienti a cui può accedere. |
| **Postcondizioni** | La terapia del paziente è creata o aggiornata nel sistema. [cite_start]Il sistema tiene traccia di quale medico ha effettuato l'operazione. |

#### Flusso Principale (Scenario di Successo)
1.  Il medico seleziona un paziente e sceglie l'opzione per gestire la sua terapia.
2.  Il sistema mostra la terapia attuale (se esiste) e fornisce le opzioni per aggiungerne una nuova o modificarla.
3.  Il medico compila i campi della terapia:
    * [cite_start]Nome del farmaco.
    * [cite_start]Numero di assunzioni giornaliere.
    * [cite_start]Quantità di farmaco per ogni assunzione.
    * [cite_start]Eventuali indicazioni aggiuntive (es. "lontano dai pasti").
4.  Il medico conferma le modifiche o il nuovo inserimento.
5.  Il sistema valida che tutti i campi obbligatori siano stati compilati.
6.  [cite_start]Il sistema salva o aggiorna la terapia per il paziente, registrando anche l'identificativo del medico che ha eseguito l'operazione.
7.  Il sistema mostra un messaggio di conferma.

#### Flussi Alternativi ed Eccezioni
* **Dati incompleti**: Se il medico non compila uno dei campi obbligatori (es. nome del farmaco), il sistema visualizza un messaggio di errore e impedisce il salvataggio fino a quando tutti i dati necessari non saranno inseriti.