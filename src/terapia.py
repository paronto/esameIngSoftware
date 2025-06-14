# src/terapia.py

class Terapia:
    """
    Rappresenta la terapia prescritta da un medico a un paziente.
    """
    def __init__(self, farmaco, assunzioni_giornaliere, quantita, indicazioni):
        # Per ogni terapia il medico specifica farmaco, numero di assunzioni giornaliere,
        # la quantità di farmaco per ogni assunzione, ed eventuali indicazioni.
        self.farmaco = farmaco
        self.assunzioni_giornaliere = assunzioni_giornaliere
        self.quantita = quantita
        self.indicazioni = indicazioni

    def __str__(self):
        return (f"Farmaco: {self.farmaco}, {self.assunzioni_giornaliere} volte al giorno, "
                f"Quantità: {self.quantita}, Indicazioni: {self.indicazioni}")