# Casi d'Uso del Sistema di Gestione Pazienti Diabetici

Questo documento descrive i casi d'uso principali del sistema, identificando gli attori e le loro interazioni principali con il software.

## 1. Attori

Gli attori che interagiscono con il sistema sono tre:

* **Paziente**: L'utilizzatore principale del sistema, che monitora la propria condizione.
* [cite_start]**Medico (Diabetologo)**: Lo specialista che segue uno o più pazienti, ne visualizza i dati e imposta le terapie.
* **Responsabile del Servizio**: Un ruolo amministrativo che gestisce le utenze del sistema.

## 2. Diagramma dei Casi d'Uso (Rappresentazione Testuale)

Di seguito sono elencati i casi d'uso per ogni attore.

### Attore: Paziente

* **UC-P01: Autenticazione**: Accede al sistema tramite credenziali personali.
* [cite_start]**UC-P02: Inserimento Dati Glicemici**: Memorizza le rilevazioni giornaliere di glicemia, specificando se prima o dopo un pasto.
* [cite_start]**UC-P03: Inserimento Sintomi**: Aggiunge eventuali sintomi riscontrati (es. spossatezza, nausea).
* [cite_start]**UC-P04: Registrazione Assunzione Farmaci**: Memorizza l'assunzione di farmaci o insulina, come da prescrizione (giorno, ora, farmaco, quantità). [cite_start]Il sistema lo invita a completare gli inserimenti se mancanti.
* [cite_start]**UC-P05: Segnalazione Terapie Concomitanti**: Segnala eventuali altre patologie o terapie in corso, specificando il periodo.
* **UC-P06: Visualizzazione Terapia**: Consulta la terapia prescritta dal medico.
* [cite_start]**UC-P07: Contatto Medico**: Invia email al proprio medico di riferimento per richieste o domande.

### Attore: Medico

* **UC-M01: Autenticazione**: Accede al sistema tramite credenziali personali.
* [cite_start]**UC-M02: Gestione Terapia**: Specifica, aggiunge o modifica la terapia per un paziente (farmaco, dosaggio, frequenza, indicazioni).
* **UC-M03: Visualizzazione Dati Paziente**:
    * [cite_start]Consulta i dati di ogni paziente.
    * [cite_start]Visualizza i dati in forma sintetica (es. andamenti settimanali/mensili).
* [cite_start]**UC-M04: Aggiornamento Anagrafica Clinica**: Aggiorna una sezione informativa del paziente con fattori di rischio, patologie pregresse o comorbidità.
* **UC-M05: Ricezione Alert**: Riceve notifiche dal sistema se:
    * [cite_start]Un paziente non segue le prescrizioni per più di 3 giorni consecutivi.
    * [cite_start]Un paziente registra valori di glicemia oltre le soglie di gravità.

### Attore: Responsabile del Servizio

* [cite_start]**UC-A01: Gestione Utenti**: Inserisce i dati iniziali di pazienti e medici necessari per la loro autenticazione.
* [cite_start]**UC-A02: Assegnazione Medico**: Specifica un medico di riferimento per ogni paziente.