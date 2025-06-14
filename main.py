# main.py

import sys
import customtkinter
sys.path.append('src')

from gui import App
from data_manager import DataManager
from admin import Admin

def setup_initial_data():
    """Crea dati iniziali se il file non esiste o è vuoto."""
    dm = DataManager('dati_clinici.json')
    _, _, admins = dm.carica_dati()
    if not admins:
        print("Nessun admin trovato. Creo l'utente admin di default.")
        admin_default = Admin(id_utente="A01", nome="Admin", cognome="System", email="admin", password="admin")
        dm.salva_dati([], [], [admin_default])

if __name__ == "__main__":
    setup_initial_data()

    # --- NUOVO TEMA GRAFICO ---
    customtkinter.set_appearance_mode("Light")
    customtkinter.set_default_color_theme("green") # Imposta il nuovo tema verde

    root = customtkinter.CTk()
    app = App(root)
    root.mainloop()