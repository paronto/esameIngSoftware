# src/paziente.py

from utente import Utente
from terapia import Terapia

class Paziente(Utente):
    """
    Rappresenta un paziente. Eredita da Utente e ha funzionalità specifiche
    per la registrazione di dati clinici.
    """
    def __init__(self, id_utente, nome, cognome, email, password, medico_riferimento_id):
        super().__init__(id_utente, nome, cognome, email, password)
        self.medico_riferimento_id = medico_riferimento_id
        self.misurazioni = []
        self.farmaci_assunti = []
        self.terapia_prescritta = None # Oggetto di tipo Terapia
        # Contiene fattori di rischio, pregresse patologie, comorbidità.
        self.info_cliniche = {}

    def __str__(self):
        return f"[Paziente] {self.nome} {self.cognome}"