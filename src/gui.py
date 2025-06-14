# src/gui.py

import customtkinter
from tkinter import ttk, messagebox
from data_manager import DataManager
from paziente import Paziente
from medico import Medico
from admin import Admin
from misurazione import Misurazione
from terapia import Terapia
from farmaco_assunto import FarmacoAssunto
import alert_manager 

# Costanti per i colori e i font per uno stile coerente
FONT_TITOLO = ("Calibri", 24, "bold")
FONT_SOTTOTITOLO = ("Calibri", 16, "bold")
FONT_NORMALE = ("Calibri", 12)
COLORE_DELETE = "#D32F2F"
COLORE_DELETE_HOVER = "#B71C1C"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Gestione Pazienti Diabetici")
        self.data_manager = DataManager('dati_clinici.json')
        self.utente_corrente = None
        self.lista_pazienti_completa = []
        self.lista_medici_completi = []
        
        # Stile per il Treeview (Admin) abbinato al nuovo tema verde
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#E0F2F1", foreground="black", rowheight=25, fieldbackground="#E0F2F1", borderwidth=0)
        style.map('Treeview', background=[('selected', '#00796B')])
        style.configure("Treeview.Heading", background="#00796B", foreground="white", font=('Calibri', 10,'bold'), borderwidth=0)

        self._crea_schermata_login()

    def _pulisci_finestra(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def _crea_schermata_login(self):
        self.root.geometry("450x400")
        self._pulisci_finestra()
        
        frame = customtkinter.CTkFrame(self.root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        customtkinter.CTkLabel(frame, text="Sistema Clinico", font=FONT_TITOLO).pack(pady=(20, 10))
        customtkinter.CTkLabel(frame, text="Accedi al tuo account", font=FONT_NORMALE).pack(pady=(0, 25))

        self.entry_email = customtkinter.CTkEntry(frame, placeholder_text="Email", height=40)
        self.entry_email.pack(pady=10, padx=10, fill="x")

        self.entry_password = customtkinter.CTkEntry(frame, placeholder_text="Password", show="*", height=40)
        self.entry_password.pack(pady=10, padx=10, fill="x")

        button = customtkinter.CTkButton(frame, text="Login", command=self._esegui_login, height=40)
        button.pack(pady=(20, 15), padx=10, fill="x")

    def _esegui_login(self):
        # ... (Logica invariata)
        email = self.entry_email.get()
        password = self.entry_password.get()
        if not email or not password:
            messagebox.showerror("Errore di Login", "Email e password non possono essere vuoti.")
            return
        
        utente = self.data_manager.autentica_utente(email, password)
        if utente:
            self.utente_corrente = utente
            if isinstance(utente, Paziente):
                self._crea_dashboard_paziente()
            elif isinstance(utente, Medico):
                self._crea_dashboard_medico()
            elif isinstance(utente, Admin):
                self._crea_dashboard_admin()
        else:
            messagebox.showerror("Errore di Login", "Credenziali non valide. Riprova.")

    def _esegui_logout(self):
        self._crea_schermata_login()

    def _crea_dashboard_paziente(self):
        self.root.geometry("600x750")
        self._pulisci_finestra()
        
        main_frame = customtkinter.CTkScrollableFrame(self.root, fg_color="transparent")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        customtkinter.CTkLabel(main_frame, text=f"Dashboard Paziente", font=FONT_TITOLO).pack(anchor="w", pady=(0,5))
        customtkinter.CTkLabel(main_frame, text=f"Benvenuto, {self.utente_corrente.nome}!", font=FONT_SOTTOTITOLO).pack(anchor="w")

        _, medici, _ = self.data_manager.carica_dati()
        medico_ref = next((m for m in medici if m.id_utente == self.utente_corrente.medico_riferimento_id), None)
        nome_medico = f"Dott. {medico_ref.cognome}" if medico_ref else "Nessuno"
        customtkinter.CTkLabel(main_frame, text=f"Medico di riferimento: {nome_medico}", font=("Calibri", 12, "italic")).pack(anchor="w", pady=(0, 20))

        # --- Sezioni separate per chiarezza ---
        self._crea_sezione_terapia_paziente(main_frame)
        self._crea_sezione_assunzione_paziente(main_frame)
        self._crea_sezione_misurazione_paziente(main_frame)
        
        customtkinter.CTkButton(main_frame, text="Logout", command=self._esegui_logout, width=120).pack(pady=20)

    def _crea_sezione_terapia_paziente(self, parent_frame):
        frame = customtkinter.CTkFrame(parent_frame)
        frame.pack(fill="x", pady=10, ipady=10)
        customtkinter.CTkLabel(frame, text="Terapia Prescritta", font=FONT_SOTTOTITOLO).pack(anchor="w", padx=15, pady=(10, 5))
        terapia = self.utente_corrente.terapia_prescritta
        testo_terapia = str(terapia) if terapia else "Nessuna terapia prescritta."
        customtkinter.CTkLabel(frame, text=testo_terapia, wraplength=500, justify="left").pack(anchor="w", padx=15, pady=(0,10))

    def _crea_sezione_assunzione_paziente(self, parent_frame):
        frame = customtkinter.CTkFrame(parent_frame)
        frame.pack(fill="x", pady=10)
        customtkinter.CTkLabel(frame, text="Registra Assunzione Farmaco", font=FONT_SOTTOTITOLO).pack(anchor="w", padx=15, pady=(10,5))
        terapia = self.utente_corrente.terapia_prescritta
        if terapia:
            customtkinter.CTkButton(frame, text=f"Conferma assunzione di {terapia.farmaco}", command=self._registra_assunzione_farmaco, height=40).pack(pady=15, padx=15, fill="x")
        else:
            customtkinter.CTkLabel(frame, text="Nessun farmaco da registrare.").pack(padx=15, pady=15, anchor="w")

    def _crea_sezione_misurazione_paziente(self, parent_frame):
        frame = customtkinter.CTkFrame(parent_frame)
        frame.pack(fill="x", pady=10, expand=True)
        frame.grid_columnconfigure(1, weight=1)
        customtkinter.CTkLabel(frame, text="Aggiungi Nuova Misurazione", font=FONT_SOTTOTITOLO).grid(row=0, column=0, columnspan=2, padx=15, pady=(10,10), sticky="w")
        customtkinter.CTkLabel(frame, text="Valore Glicemia (mg/dL):").grid(row=1, column=0, sticky="w", padx=15, pady=5)
        self.entry_glicemia = customtkinter.CTkEntry(frame)
        self.entry_glicemia.grid(row=1, column=1, sticky="ew", padx=15, pady=5)
        customtkinter.CTkLabel(frame, text="Momento:").grid(row=2, column=0, sticky="w", padx=15, pady=5)
        opzioni_momento = ["prima colazione", "dopo colazione", "prima pranzo", "dopo pranzo", "prima cena", "dopo cena"]
        self.momento_selezionato = customtkinter.CTkOptionMenu(frame, values=opzioni_momento)
        self.momento_selezionato.grid(row=2, column=1, sticky="ew", padx=15, pady=5)
        customtkinter.CTkLabel(frame, text="Sintomi (opzionale):").grid(row=3, column=0, sticky="w", padx=15, pady=5)
        self.entry_sintomi = customtkinter.CTkEntry(frame, placeholder_text="es. spossatezza, nausea...")
        self.entry_sintomi.grid(row=3, column=1, sticky="ew", padx=15, pady=5)
        customtkinter.CTkButton(frame, text="Salva Misurazione", command=self._salva_nuova_misurazione, height=40).grid(row=4, column=0, columnspan=2, pady=15, padx=15, sticky="ew")

    def _registra_assunzione_farmaco(self):
        # ... (Logica invariata)
        terapia_corrente = self.utente_corrente.terapia_prescritta
        if not terapia_corrente:
            messagebox.showerror("Errore", "Nessuna terapia prescritta da registrare.")
            return
        nuova_assunzione = FarmacoAssunto(
            farmaco_nome=terapia_corrente.farmaco,
            quantita=terapia_corrente.quantita
        )
        pazienti, medici, admins = self.data_manager.carica_dati()
        for p in pazienti:
            if p.id_utente == self.utente_corrente.id_utente:
                if not hasattr(p, 'farmaci_assunti') or p.farmaci_assunti is None:
                    p.farmaci_assunti = []
                p.farmaci_assunti.append(nuova_assunzione)
                self.utente_corrente = p
                break
        self.data_manager.salva_dati(pazienti, medici, admins)
        messagebox.showinfo("Successo", f"Assunzione di {terapia_corrente.farmaco} registrata correttamente!")

    def _salva_nuova_misurazione(self):
        # ... (Logica invariata)
        valore_str = self.entry_glicemia.get()
        momento = self.momento_selezionato.get()
        sintomi_str = self.entry_sintomi.get()
        if not valore_str:
            messagebox.showwarning("Dati mancanti", "Il valore della glicemia è obbligatorio.")
            return
        try:
            valore = int(valore_str)
        except ValueError:
            messagebox.showerror("Errore", "Il valore della glicemia deve essere un numero.")
            return
        sintomi = sintomi_str.split(',') if sintomi_str else []
        nuova_misurazione = Misurazione(valore_glicemia=valore, momento=momento, sintomi=sintomi)
        alert_msg = alert_manager.controlla_glicemia_alta(nuova_misurazione)
        if alert_msg:
            messagebox.showwarning("Allarme Glicemia", alert_msg)
        pazienti, medici, admins = self.data_manager.carica_dati()
        for p in pazienti:
            if p.id_utente == self.utente_corrente.id_utente:
                p.misurazioni.append(nuova_misurazione)
                self.utente_corrente = p 
                break
        self.data_manager.salva_dati(pazienti, medici, admins)
        messagebox.showinfo("Successo", "Misurazione salvata correttamente!")
        self.entry_glicemia.delete(0, customtkinter.END)
        self.entry_sintomi.delete(0, customtkinter.END)

    def _crea_dashboard_medico(self):
        self.root.geometry("1100x750")
        self._pulisci_finestra()
        
        main_frame = customtkinter.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        main_frame.grid_columnconfigure(1, weight=3)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        customtkinter.CTkLabel(main_frame, text=f"Dashboard Medico", font=FONT_TITOLO).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0,5))
        customtkinter.CTkLabel(main_frame, text=f"Dott. {self.utente_corrente.cognome}", font=FONT_SOTTOTITOLO).grid(row=0, column=1, sticky="w", padx=(180,0), pady=(0,5))

        # Colonna sinistra
        left_frame = customtkinter.CTkFrame(main_frame)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        customtkinter.CTkLabel(left_frame, text="I Miei Pazienti:", font=FONT_SOTTOTITOLO).pack(anchor="w", padx=15, pady=10)
        self.pazienti_scroll_frame = customtkinter.CTkScrollableFrame(left_frame, label_text="")
        self.pazienti_scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Colonna destra
        self.right_frame = customtkinter.CTkFrame(main_frame)
        self.right_frame.grid(row=1, column=1, sticky="nsew")
        customtkinter.CTkLabel(self.right_frame, text="Seleziona un paziente dalla lista.", font=FONT_NORMALE).pack(expand=True)
        
        self._popola_lista_pazienti_medico()
        
        # Logout in fondo
        customtkinter.CTkButton(self.root, text="Logout", command=self._esegui_logout, width=120).pack(side="bottom", pady=10)

        # Controlliamo gli alert dopo aver costruito l'interfaccia
        tutti_i_pazienti, _, _ = self.data_manager.carica_dati()
        pazienti_del_medico = [p for p in tutti_i_pazienti if p.medico_riferimento_id == self.utente_corrente.id_utente]
        alerts_terapia = alert_manager.controlla_mancata_assunzione(pazienti_del_medico)
        if alerts_terapia:
            messaggio_completo = "Sono presenti i seguenti allarmi per i tuoi pazienti:\n\n" + "\n".join(alerts_terapia)
            messagebox.showwarning("Allarmi Terapia", messaggio_completo)

    def _popola_lista_pazienti_medico(self):
        for widget in self.pazienti_scroll_frame.winfo_children():
            widget.destroy()

        tutti_i_pazienti, _, _ = self.data_manager.carica_dati()
        self.lista_pazienti_del_medico = [p for p in tutti_i_pazienti if p.medico_riferimento_id == self.utente_corrente.id_utente]
        
        # Memorizza i bottoni per cambiare stile al click
        self.pazienti_buttons = []
        if not self.lista_pazienti_del_medico:
            customtkinter.CTkLabel(self.pazienti_scroll_frame, text="Nessun paziente assegnato.").pack()
        else:
            for paziente in self.lista_pazienti_del_medico:
                btn = customtkinter.CTkButton(self.pazienti_scroll_frame, text=f"{paziente.cognome}, {paziente.nome}", 
                                              fg_color="transparent", border_width=1,
                                              command=lambda p=paziente: self._seleziona_paziente_medico(p))
                btn.pack(fill="x", pady=2)
                self.pazienti_buttons.append(btn)

    def _seleziona_paziente_medico(self, paziente):
        # Evidenzia il pulsante selezionato
        for btn in self.pazienti_buttons:
            if paziente.cognome in btn.cget("text"):
                btn.configure(fg_color=("#3A7EBF", "#1F538D")) # Colore primario del tema
            else:
                btn.configure(fg_color="transparent")
        self._mostra_dettagli_paziente(paziente)

    def _mostra_dettagli_paziente(self, paziente_selezionato):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Usiamo uno scrollable frame anche per i dettagli
        detail_scroll_frame = customtkinter.CTkScrollableFrame(self.right_frame, fg_color="transparent")
        detail_scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        customtkinter.CTkLabel(detail_scroll_frame, text=f"Dettagli: {paziente_selezionato.nome} {paziente_selezionato.cognome}", font=FONT_SOTTOTITOLO).pack(anchor="w", padx=10, pady=5)
        
        # ... (il resto della logica è simile, ma inserita nello scroll frame)
        frame_misurazioni = customtkinter.CTkFrame(detail_scroll_frame)
        frame_misurazioni.pack(fill="x", padx=10, pady=5)
        customtkinter.CTkLabel(frame_misurazioni, text="Misurazioni Recenti", font=FONT_NORMALE).pack(anchor="w", padx=10, pady=5)
        m_sub_scroll_frame = customtkinter.CTkScrollableFrame(frame_misurazioni, height=150)
        m_sub_scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)
        if paziente_selezionato.misurazioni:
            for mis in reversed(paziente_selezionato.misurazioni):
                customtkinter.CTkLabel(m_sub_scroll_frame, text=str(mis)).pack(anchor="w", padx=2)
        else:
            customtkinter.CTkLabel(m_sub_scroll_frame, text="Nessuna misurazione registrata.").pack()

        frame_terapia = customtkinter.CTkFrame(detail_scroll_frame)
        frame_terapia.pack(fill="x", padx=10, pady=5)
        frame_terapia.grid_columnconfigure(1, weight=1)
        self.label_gestione_terapia = customtkinter.CTkLabel(frame_terapia, text="Gestione Terapia", font=FONT_NORMALE)
        self.label_gestione_terapia.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        
        terapia_attuale = paziente_selezionato.terapia_prescritta
        self.label_terapia_attuale = customtkinter.CTkLabel(frame_terapia, text=f"Attuale: {str(terapia_attuale) if terapia_attuale else 'Nessuna'}", wraplength=400)
        self.label_terapia_attuale.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        
        self.entry_farmaco = customtkinter.CTkEntry(frame_terapia, placeholder_text="Nome farmaco")
        self.entry_farmaco.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.entry_assunzioni = customtkinter.CTkEntry(frame_terapia, placeholder_text="Assunzioni al giorno (es. 2)")
        self.entry_assunzioni.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        self.entry_quantita = customtkinter.CTkEntry(frame_terapia, placeholder_text="Quantità (es. 500mg)")
        self.entry_quantita.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        self.entry_indicazioni = customtkinter.CTkEntry(frame_terapia, placeholder_text="Indicazioni aggiuntive")
        self.entry_indicazioni.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        if terapia_attuale:
            self.entry_farmaco.insert(0, terapia_attuale.farmaco)
            self.entry_assunzioni.insert(0, terapia_attuale.assunzioni_giornaliere)
            self.entry_quantita.insert(0, terapia_attuale.quantita)
            self.entry_indicazioni.insert(0, terapia_attuale.indicazioni)

        customtkinter.CTkButton(frame_terapia, text="Aggiorna Terapia", command=lambda: self._aggiorna_terapia(paziente_selezionato), height=40).grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    def _aggiorna_terapia(self, paziente_da_aggiornare):
        # ... (Logica di aggiornamento e salvataggio invariata)
        farmaco = self.entry_farmaco.get()
        assunzioni_str = self.entry_assunzioni.get()
        quantita = self.entry_quantita.get()
        indicazioni = self.entry_indicazioni.get()
        if not all([farmaco, assunzioni_str, quantita]):
            messagebox.showwarning("Dati mancanti", "Compilare almeno Farmaco, Assunzioni e Quantità.")
            return
        try:
            assunzioni_num = int(assunzioni_str)
        except ValueError:
            messagebox.showerror("Errore di Input", "Il campo 'Assunzioni/giorno' deve contenere solo un numero.")
            return
        
        nuova_terapia = Terapia(farmaco, assunzioni_num, quantita, indicazioni)
        
        pazienti, medici, admins = self.data_manager.carica_dati()
        paziente_trovato_in_lista = None
        for p in pazienti:
            if p.id_utente == paziente_da_aggiornare.id_utente:
                self.utente_corrente.prescrivi_terapia(p, nuova_terapia)
                paziente_trovato_in_lista = p # Memorizziamo l'oggetto aggiornato
                break
        
        self.data_manager.salva_dati(pazienti, medici, admins)
        messagebox.showinfo("Successo", f"Terapia per {paziente_da_aggiornare.nome} aggiornata.")

        # Aggiornamento istantaneo della GUI
        if paziente_trovato_in_lista:
            self.label_terapia_attuale.configure(text=f"Attuale: {str(paziente_trovato_in_lista.terapia_prescritta)}")

    # ... (il resto della classe, con i metodi per l'admin, rimane invariato)
    def _crea_dashboard_admin(self):
        self.root.geometry("1100x700")
        self._pulisci_finestra()
        customtkinter.CTkLabel(self.root, text=f"Pannello Amministratore", font=FONT_TITOLO).pack(pady=10, padx=20, anchor="w")
        action_frame = customtkinter.CTkFrame(self.root, fg_color="transparent")
        action_frame.pack(fill="x", padx=20, pady=5)
        customtkinter.CTkButton(action_frame, text="Crea Paziente", command=self._crea_nuovo_paziente_dialog).pack(side="left", padx=5)
        customtkinter.CTkButton(action_frame, text="Crea Medico", command=self._crea_nuovo_medico_dialog).pack(side="left", padx=5)
        
        main_frame = customtkinter.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_rowconfigure(0, weight=1)
        
        tree_frame = customtkinter.CTkFrame(main_frame)
        tree_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Email"), show="headings")
        self.tree.pack(side="left", fill="both", expand=True)
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.heading("ID", text="ID Utente")
        self.tree.heading("Email", text="Email")
        self.tree.bind("<<TreeviewSelect>>", self._mostra_dettagli_admin_view)
        
        self.admin_detail_frame = customtkinter.CTkFrame(main_frame)
        self.admin_detail_frame.grid(row=0, column=1, sticky="nsew")
        
        self._popola_vista_admin()
        customtkinter.CTkButton(self.root, text="Logout", command=self._esegui_logout, width=120).pack(side="bottom", pady=20)
    
    def _popola_vista_admin(self):
        # ... (Invariato)
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.lista_pazienti_completa, self.lista_medici_completi, _ = self.data_manager.carica_dati()
        pazienti_non_assegnati = [p for p in self.lista_pazienti_completa if p.medico_riferimento_id is None]
        for medico in self.lista_medici_completi:
            medico_id = self.tree.insert("", "end", text=f"Dr. {medico.cognome}", values=(medico.id_utente, medico.email), open=True, tags=('medico',))
            for paziente in self.lista_pazienti_completa:
                if paziente.medico_riferimento_id == medico.id_utente:
                    self.tree.insert(medico_id, "end", text=f"  {paziente.cognome}, {paziente.nome}", values=(paziente.id_utente, paziente.email), tags=('paziente',))
        if pazienti_non_assegnati:
            unassigned_id = self.tree.insert("", "end", text="Pazienti non Assegnati", open=True, tags=('non_assegnato',))
            for paziente in pazienti_non_assegnati:
                self.tree.insert(unassigned_id, "end", text=f"  {paziente.cognome}, {paziente.nome}", values=(paziente.id_utente, paziente.email), tags=('paziente',))

    def _mostra_dettagli_admin_view(self, event=None):
        # ... (Invariato)
        for widget in self.admin_detail_frame.winfo_children():
            widget.destroy()
        selection = self.tree.selection()
        if not selection:
            return
        item_id = selection[0]
        item_tags = self.tree.item(item_id, "tags")
        item_values = self.tree.item(item_id, "values")
        user_id = item_values[0]
        if 'paziente' in item_tags:
            paziente_selezionato = next((p for p in self.lista_pazienti_completa if p.id_utente == user_id), None)
            if paziente_selezionato:
                customtkinter.CTkLabel(self.admin_detail_frame, text="Azioni Paziente", font=FONT_SOTTOTITOLO).pack(anchor="w", padx=15, pady=10)
                customtkinter.CTkButton(self.admin_detail_frame, text="Sposta Paziente", command=lambda: self._sposta_paziente_dialog(paziente_selezionato)).pack(pady=5, padx=15, fill="x")
                customtkinter.CTkButton(self.admin_detail_frame, text="Terapia Conclusa (Elimina)", fg_color=COLORE_DELETE, hover_color=COLORE_DELETE_HOVER, command=lambda: self._elimina_utente(paziente_selezionato, "Paziente")).pack(pady=5, padx=15, fill="x")
        elif 'medico' in item_tags:
            medico_selezionato = next((m for m in self.lista_medici_completi if m.id_utente == user_id), None)
            if medico_selezionato:
                customtkinter.CTkLabel(self.admin_detail_frame, text="Azioni Medico", font=FONT_SOTTOTITOLO).pack(anchor="w", padx=15, pady=10)
                customtkinter.CTkButton(self.admin_detail_frame, text="Servizio Terminato (Elimina)", fg_color=COLORE_DELETE, hover_color=COLORE_DELETE_HOVER, command=lambda: self._elimina_utente(medico_selezionato, "Medico")).pack(pady=5, padx=15, fill="x")
                
                terapie_frame = customtkinter.CTkFrame(self.admin_detail_frame)
                terapie_frame.pack(fill="both", expand=True, pady=10, padx=15)
                customtkinter.CTkLabel(terapie_frame, text="Terapie Prescritte", font=FONT_NORMALE).pack(anchor="w", padx=10, pady=5)
                t_scroll_frame = customtkinter.CTkScrollableFrame(terapie_frame)
                t_scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)
                terapie_prescritte = []
                for p in self.lista_pazienti_completa:
                    if p.terapia_prescritta and hasattr(p.terapia_prescritta, 'medico_prescrittore_id') and p.terapia_prescritta.medico_prescrittore_id == medico_selezionato.id_utente:
                        info_terapia = f"Paziente: {p.cognome} - {p.terapia_prescritta}"
                        terapie_prescritte.append(info_terapia)
                if terapie_prescritte:
                    for terapia_info in terapie_prescritte:
                        customtkinter.CTkLabel(t_scroll_frame, text=terapia_info, wraplength=350).pack(anchor="w", padx=5)
                else:
                    customtkinter.CTkLabel(t_scroll_frame, text="Nessuna terapia prescritta da questo medico.").pack()
    
    def _elimina_utente(self, utente_da_eliminare, tipo_utente):
        # ... (Invariato)
        conferma = messagebox.askyesno(
            "Conferma Eliminazione",
            f"Sei sicuro di voler eliminare {tipo_utente.lower()} {utente_da_eliminare.nome} {utente_da_eliminare.cognome}?\n\nL'azione è irreversibile.",
            icon='warning'
        )
        if not conferma:
            return 
        pazienti, medici, admins = self.data_manager.carica_dati()
        if tipo_utente == "Paziente":
            pazienti_aggiornati = [p for p in pazienti if p.id_utente != utente_da_eliminare.id_utente]
            self.data_manager.salva_dati(pazienti_aggiornati, medici, admins)
        elif tipo_utente == "Medico":
            medici_aggiornati = [m for m in medici if m.id_utente != utente_da_eliminare.id_utente]
            for p in pazienti:
                if p.medico_riferimento_id == utente_da_eliminare.id_utente:
                    p.medico_riferimento_id = None
            self.data_manager.salva_dati(pazienti, medici_aggiornati, admins)
        messagebox.showinfo("Successo", f"{tipo_utente} eliminato con successo.")
        self._popola_vista_admin()
        for widget in self.admin_detail_frame.winfo_children():
            widget.destroy()

    def _crea_nuovo_utente_dialog(self, tipo_utente):
        # ... (Invariato)
        dialog = customtkinter.CTkToplevel(self.root)
        dialog.title(f"Crea Nuovo {tipo_utente}")
        dialog.geometry("350x300")
        dialog.transient(self.root)
        dialog.grid_columnconfigure(1, weight=1)
        customtkinter.CTkLabel(dialog, text="Nome:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        entry_nome = customtkinter.CTkEntry(dialog)
        entry_nome.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        customtkinter.CTkLabel(dialog, text="Cognome:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        entry_cognome = customtkinter.CTkEntry(dialog)
        entry_cognome.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        customtkinter.CTkLabel(dialog, text="Email:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        entry_email = customtkinter.CTkEntry(dialog)
        entry_email.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        customtkinter.CTkLabel(dialog, text="Password:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        entry_password = customtkinter.CTkEntry(dialog, show="*")
        entry_password.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        def salva_utente():
            nome = entry_nome.get()
            cognome = entry_cognome.get()
            email = entry_email.get()
            password = entry_password.get()
            if not all([nome, cognome, email, password]):
                messagebox.showerror("Errore", "Tutti i campi sono obbligatori.", parent=dialog)
                return
            pazienti, medici, admins = self.data_manager.carica_dati()
            if tipo_utente == "Paziente":
                nuovo_id = f"P{len(pazienti) + len(medici) + 100}" 
                nuovo_paziente = Paziente(nuovo_id, nome, cognome, email, password, medico_riferimento_id=None)
                pazienti.append(nuovo_paziente)
            else: 
                nuovo_id = f"M{len(pazienti) + len(medici) + 100}"
                nuovo_medico = Medico(nuovo_id, nome, cognome, email, password)
                medici.append(nuovo_medico)
            self.data_manager.salva_dati(pazienti, medici, admins)
            messagebox.showinfo("Successo", f"{tipo_utente} creato con successo!", parent=dialog)
            self._popola_vista_admin() 
            dialog.destroy()
        customtkinter.CTkButton(dialog, text="Salva", command=salva_utente, height=40).grid(row=4, column=0, columnspan=2, pady=20, padx=10, sticky="ew")

    def _crea_nuovo_paziente_dialog(self):
        self._crea_nuovo_utente_dialog("Paziente")

    def _crea_nuovo_medico_dialog(self):
        self._crea_nuovo_utente_dialog("Medico")

    def _sposta_paziente_dialog(self, paziente):
        # ... (Invariato)
        dialog = customtkinter.CTkToplevel(self.root)
        dialog.title(f"Sposta Paziente")
        dialog.geometry("350x180")
        dialog.transient(self.root)
        customtkinter.CTkLabel(dialog, text=f"Sposta {paziente.cognome} al medico:").pack(padx=10, pady=10)
        nomi_medici = [f"{m.id_utente}: {m.cognome}" for m in self.lista_medici_completi]
        scelta_medico = customtkinter.CTkComboBox(dialog, values=nomi_medici, height=40)
        scelta_medico.pack(padx=10, pady=5, fill="x")
        scelta_medico.set("Seleziona un medico")
        def conferma_spostamento():
            scelta = scelta_medico.get()
            if "Seleziona" in scelta:
                messagebox.showerror("Errore", "Nessun medico selezionato.", parent=dialog)
                return
            nuovo_medico_id = scelta.split(':')[0]
            pazienti, medici, admins = self.data_manager.carica_dati()
            for p in pazienti:
                if p.id_utente == paziente.id_utente:
                    p.medico_riferimento_id = nuovo_medico_id
                    break
            self.data_manager.salva_dati(pazienti, medici, admins)
            messagebox.showinfo("Successo", "Paziente spostato con successo.", parent=dialog)
            self._popola_vista_admin()
            dialog.destroy()
        customtkinter.CTkButton(dialog, text="Conferma", command=conferma_spostamento, height=40).pack(pady=10, padx=10, fill="x")