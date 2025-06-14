# src/utente.py

class Utente:
    """
    Classe base per tutti gli utenti del sistema.
    Contiene le informazioni comuni a Pazienti e Medici.
    """
    def __init__(self, id_utente, nome, cognome, email, password):
        self.id_utente = id_utente
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.password = password # Necessario per l'autenticazione

    def __str__(self):
        return f"{self.nome} {self.cognome}"