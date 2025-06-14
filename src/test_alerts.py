# src/test_alerts.py

import unittest
from datetime import datetime, timedelta

# Importiamo le funzioni e le classi da testare
import alert_manager
from misurazione import Misurazione
from paziente import Paziente
from terapia import Terapia
from farmaco_assunto import FarmacoAssunto

class TestAlertManager(unittest.TestCase):
    """
    Suite di test per il nostro sistema di alert.
    Ogni metodo che inizia con 'test_' è un singolo caso di test.
    """

    def test_alert_glicemia_critica(self):
        """Verifica che un valore di glicemia molto alto generi un alert critico."""
        print("\nEseguo test: Glicemia Critica...")
        misurazione_critica = Misurazione(valore_glicemia=300, momento="dopo pranzo")
        messaggio = alert_manager.controlla_glicemia_alta(misurazione_critica)
        self.assertIn("ALERT CRITICO", messaggio) # Verifichiamo che la stringa contenga il testo atteso

    def test_alert_glicemia_alta_dopo_pasto(self):
        """Verifica che un valore alto dopo un pasto generi un alert."""
        print("Eseguo test: Glicemia Alta (Post-pasto)...")
        misurazione_alta = Misurazione(valore_glicemia=190, momento="dopo cena")
        messaggio = alert_manager.controlla_glicemia_alta(misurazione_alta)
        self.assertIn("post-pasto elevato", messaggio)

    def test_nessun_alert_glicemia_normale(self):
        """Verifica che un valore normale non generi alcun alert."""
        print("Eseguo test: Glicemia Normale...")
        misurazione_normale = Misurazione(valore_glicemia=120, momento="dopo pranzo")
        messaggio = alert_manager.controlla_glicemia_alta(misurazione_normale)
        self.assertIsNone(messaggio) # Verifichiamo che il risultato sia None (nessun alert)

    def test_alert_mancata_assunzione(self):
        """Verifica che l'alert si attivi se non ci sono assunzioni da più di 3 giorni."""
        print("Eseguo test: Mancata Assunzione Farmaci...")
        # Creiamo un paziente fittizio (mock) per il test
        paziente_test = Paziente("P_TEST", "Test", "User", "t@u.it", "p", "M01")
        paziente_test.terapia_prescritta = Terapia("Test-Farmaco", 1, "1", "")
        
        # Aggiungiamo un'assunzione di 5 giorni fa
        assunzione_vecchia = FarmacoAssunto("Test-Farmaco", "1")
        assunzione_vecchia.data_ora = datetime.now() - timedelta(days=5)
        paziente_test.farmaci_assunti.append(assunzione_vecchia)

        alerts = alert_manager.controlla_mancata_assunzione([paziente_test])
        self.assertEqual(len(alerts), 1) # Ci aspettiamo esattamente 1 alert
        self.assertIn("da più di 3 giorni", alerts[0])

    def test_nessun_alert_assunzione_recente(self):
        """Verifica che l'alert NON si attivi se c'è un'assunzione recente."""
        print("Eseguo test: Assunzione Recente...")
        paziente_test = Paziente("P_TEST", "Test", "User", "t@u.it", "p", "M01")
        paziente_test.terapia_prescritta = Terapia("Test-Farmaco", 1, "1", "")
        
        # Aggiungiamo un'assunzione di ieri
        assunzione_recente = FarmacoAssunto("Test-Farmaco", "1")
        assunzione_recente.data_ora = datetime.now() - timedelta(days=1)
        paziente_test.farmaci_assunti.append(assunzione_recente)

        alerts = alert_manager.controlla_mancata_assunzione([paziente_test])
        self.assertEqual(len(alerts), 0) # Ci aspettiamo 0 alert

# Questo blocco permette di eseguire i test direttamente dal terminale
if __name__ == '__main__':
    unittest.main()