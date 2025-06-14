# src/farmaco_assunto.py

from datetime import datetime

class FarmacoAssunto:
    """
    Rappresenta una singola assunzione di un farmaco da parte del paziente.
    """
    def __init__(self, farmaco_nome, quantita):
        # Il paziente registra le assunzioni di farmaci (giorno, ora, farmaco e quantità).
        self.farmaco_nome = farmaco_nome
        self.quantita = quantita
        self.data_ora = datetime.now()

    def __str__(self):
        return (f"{self.data_ora.strftime('%Y-%m-%d %H:%M')}: "
                f"Assunto {self.farmaco_nome}, quantità: {self.quantita}")