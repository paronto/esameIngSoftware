# src/alert_manager.py

from datetime import datetime, timedelta

def controlla_glicemia_alta(misurazione):
    """
    Controlla una singola misurazione e restituisce un messaggio di alert se supera le soglie.
    Le soglie sono definite nelle specifiche del progetto.
    """
    # Livelli di soglia
    SOGLIA_ALTA_DOPO_PASTO = 180
    SOGLIA_ALTA_PRIMA_PASTO = 130
    SOGLIA_CRITICA = 250 # Definiamo una soglia critica per maggiore gravità

    valore = misurazione.valore_glicemia
    momento = misurazione.momento

    messaggio_alert = None

    if valore > SOGLIA_CRITICA:
        messaggio_alert = f"ALERT CRITICO: Rilevato valore glicemico di {valore} mg/dL!"
    elif "dopo" in momento and valore > SOGLIA_ALTA_DOPO_PASTO:
        messaggio_alert = f"Attenzione: Valore glicemico post-pasto elevato ({valore} mg/dL)."
    elif "prima" in momento and valore > SOGLIA_ALTA_PRIMA_PASTO:
        messaggio_alert = f"Attenzione: Valore glicemico pre-pasto elevato ({valore} mg/dL)."

    return messaggio_alert

def controlla_mancata_assunzione(lista_pazienti):
    """
    Controlla tutti i pazienti e genera alert se non assumono farmaci per più di 3 giorni.
    Questo simula la richiesta "nel caso il paziente non segua per più di 3 giorni consecutivi le prescrizioni".
    """
    alerts = []
    oggi = datetime.now()

    for paziente in lista_pazienti:
        # Controlliamo solo i pazienti che hanno una terapia prescritta
        if not paziente.terapia_prescritta:
            continue

        # Troviamo la data dell'ultima assunzione di farmaci registrata
        if not paziente.farmaci_assunti:
            # Se non ha mai assunto farmaci ma ha una terapia, potrebbero essere passati più di 3 giorni
            # Per questo progetto, generiamo un alert semplice.
            alerts.append(f"ALERT Terapia: Il paziente {paziente.cognome} ha una terapia ma nessuna assunzione registrata.")
            continue
        
        # Ordiniamo le assunzioni per trovare la più recente
        ultima_assunzione = max(p.data_ora for p in paziente.farmaci_assunti)

        if (oggi - ultima_assunzione).days > 3:
            alerts.append(f"ALERT Terapia: Il paziente {paziente.cognome} non registra assunzioni da più di 3 giorni.")
            
    return alerts