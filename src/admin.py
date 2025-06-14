# src/admin.py
from utente import Utente

class Admin(Utente):
    """
    Rappresenta un utente Amministratore con privilegi speciali.
    """
    def __init__(self, id_utente, nome, cognome, email, password):
        super().__init__(id_utente, nome, cognome, email, password)

    def __str__(self):
        return f"[Admin] {self.nome} {self.cognome}"