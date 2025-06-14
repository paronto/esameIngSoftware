# src/medico.py

from utente import Utente
from terapia import Terapia

class Medico(Utente):
    def __init__(self, id_utente, nome, cognome, email, password):
        super().__init__(id_utente, nome, cognome, email, password)

    def prescrivi_terapia(self, paziente, terapia: Terapia):
        """Assegna la terapia al paziente e la 'firma' con il proprio ID."""
        # --- MODIFICA: Aggiungiamo la tracciabilità del medico ---
        terapia.medico_prescrittore_id = self.id_utente
        
        paziente.terapia_prescritta = terapia
        print(f"Il Dott. {self.cognome} ha prescritto una terapia a {paziente.nome}.")

    def __str__(self):
        return f"[Medico] {self.nome} {self.cognome} (ID: {self.id_utente})"