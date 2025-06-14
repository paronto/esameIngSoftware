# src/misurazione.py

from datetime import datetime

class Misurazione:
    """
    Rappresenta una singola misurazione glicemica del paziente.
    """
    def __init__(self, valore_glicemia, momento, sintomi=None):
        # Il paziente potrà memorizzare le rilevazioni giornaliere di glicemia.
        self.valore_glicemia = valore_glicemia
        self.momento = momento  # Es. "prima colazione", "dopo pranzo"
        # Il paziente può, inoltre, aggiungere eventuali sintomi.
        self.sintomi = sintomi if sintomi else []
        self.data_ora = datetime.now()

    def __str__(self):
        return (f"{self.data_ora.strftime('%Y-%m-%d %H:%M')}: "
                f"{self.valore_glicemia} mg/dL ({self.momento})")