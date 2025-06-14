# src/data_manager.py

import json
from datetime import datetime

# Importiamo tutte le nostre classi, inclusa la nuova classe Admin
from utente import Utente
from paziente import Paziente
from medico import Medico
from admin import Admin # <-- NUOVA IMPORTAZIONE
from terapia import Terapia
from misurazione import Misurazione
from farmaco_assunto import FarmacoAssunto

class DataManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def _converti_oggetto_in_dizionario(self, obj):
        # Aggiungiamo Admin alla lista di oggetti da convertire
        if isinstance(obj, (Paziente, Medico, Admin, Utente, Terapia, Misurazione, FarmacoAssunto)): # <-- AGGIUNTO Admin
            dizionario = {'__class__': obj.__class__.__name__}
            dizionario.update(obj.__dict__)
            return dizionario
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"L'oggetto {obj} di tipo {type(obj)} non è serializzabile in JSON")

    # ... il metodo _converti_dizionario_in_oggetto non necessita modifiche ...
    def _converti_dizionario_in_oggetto(self, dizionario):
        if '__class__' in dizionario:
            class_name = dizionario.pop('__class__')
            cls = globals().get(class_name)
            if cls:
                obj = cls.__new__(cls)
                for key, value in dizionario.items():
                    if isinstance(value, str):
                        try:
                            setattr(obj, key, datetime.fromisoformat(value))
                        except ValueError:
                            setattr(obj, key, value)
                    else:
                        setattr(obj, key, value)
                return obj
        return dizionario


    # Modifichiamo salva_dati e carica_dati per includere gli admin
    def salva_dati(self, pazienti, medici, admins):
        """Salva le liste di pazienti, medici e admin nel file JSON."""
        print(f"Salvataggio dati su {self.file_path}...")
        dati_da_salvare = {
            'pazienti': pazienti,
            'medici': medici,
            'admins': admins # <-- NUOVA CHIAVE
        }
        with open(self.file_path, 'w') as file:
            json.dump(dati_da_salvare, file, default=self._converti_oggetto_in_dizionario, indent=4)
        print("Salvataggio completato.")

    def carica_dati(self):
        """Carica i dati dal file JSON e li riconverte in oggetti."""
        try:
            with open(self.file_path, 'r') as file:
                dati_grezzi = json.load(file, object_hook=self._converti_dizionario_in_oggetto)
                pazienti = dati_grezzi.get('pazienti', [])
                medici = dati_grezzi.get('medici', [])
                admins = dati_grezzi.get('admins', []) # <-- CARICA ADMIN
                return pazienti, medici, admins
        except (FileNotFoundError, json.JSONDecodeError):
            return [], [], [] # <-- RESTITUISCE LISTA VUOTA ANCHE PER ADMIN

    # Modifichiamo l'autenticazione per riconoscere l'admin
    def autentica_utente(self, email, password):
        """Verifica le credenziali di un utente (paziente, medico o admin)."""
        pazienti, medici, admins = self.carica_dati()

        # Cerca tra gli admin
        for admin in admins:
            if admin.email == email and admin.password == password:
                print(f"Autenticazione riuscita per l'admin {admin.nome}.")
                return admin

        # Cerca tra i medici
        for medico in medici:
            if medico.email == email and medico.password == password:
                print(f"Autenticazione riuscita per il medico {medico.nome} {medico.cognome}.")
                return medico

        # Cerca tra i pazienti
        for paziente in pazienti:
            if paziente.email == email and paziente.password == password:
                print(f"Autenticazione riuscita per il paziente {paziente.nome} {paziente.cognome}.")
                return paziente

        print("Autenticazione fallita: credenziali non valide.")
        return None