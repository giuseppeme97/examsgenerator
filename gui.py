import wx
import threading
import time

class BackgroundTaskThread(threading.Thread):
    def __init__(self, parent_frame):
        threading.Thread.__init__(self)
        self.parent_frame = parent_frame
        self.daemon = True

    def run(self):
        # Simuliamo un task in background
        # ******************* #
        time.sleep(3)
        wx.CallAfter(self.parent_frame.task_completed)

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)
        self.panel = wx.Panel(self)
        self.create_widgets()
        self.setup_layout()
        self.SetSize((600, 800))


    def create_widgets(self):
        # Pulsante per la selezione della sorgente dati.
        self.file_button = wx.Button(self.panel, label="File sorgente...", style=wx.BU_LEFT)
        self.file_button.Bind(wx.EVT_BUTTON, self.on_choose_file)
        self.file_path_label = wx.StaticText(self.panel, label="Path della sorgente:")

        # Pulsante per la selezione della destinazione degli esami.
        self.folder_button = wx.Button(self.panel, label="Cartella destinazione...", style=wx.BU_LEFT)
        self.folder_button.Bind(wx.EVT_BUTTON, self.on_choose_folder)
        self.folder_path_label = wx.StaticText(self.panel, label="Path della destinazione:")

        # Input per l'inserimento dei nomi degli esami.
        self.filename_text = wx.TextCtrl(self.panel)

        # Selection per la scelta della materia.
        self.materia_choices = ["SISTEMI E RETI", "TPSIT", "INFORMATICA"]
        self.materia_dropdown = wx.Choice(self.panel, choices=self.materia_choices)

        # Selection per la scelta della classe.
        self.classe_choices = ["3^", "4^", "5^"]
        self.classe_dropdown = wx.Choice(self.panel, choices=self.classe_choices)

        # Checkboxs per la scelta delle ere.
        self.era_checkboxes = [wx.CheckBox(self.panel, label=f"Era {i}") for i in range(1, 4)]

        # Selection per la scelta del tipo di domande.
        self.type_choices = ["TEORIA", "PRATICO"]
        self.type_dropdown = wx.Choice(self.panel, choices=self.type_choices)

        # Input per l'inserimento del numero di esami da generare.
        self.exams_number = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)

        # Input per l'inserimento del numero di domande da inserire in ogni esame.
        self.questions_number = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)

        # Checkbox per le opzioni di generazione degli esami.
        self.numera_domande_checkbox = wx.CheckBox(self.panel, label="Numera domande")
        self.mescola_domande_checkbox = wx.CheckBox(self.panel, label="Mescola domande")
        self.mescola_opzioni_checkbox = wx.CheckBox(self.panel, label="Mescola opzioni")

        # Linea di separazione.
        self.separator_line = wx.StaticLine(self.panel, style=wx.LI_HORIZONTAL)
        
        # Pulsante per avviare la generazione degli esami.
        self.start_button = wx.Button(self.panel, label="Genera!", style=wx.BU_LEFT)
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start_button)

        # Barra di avanzamento.
        self.progress_bar = wx.Gauge(self.panel, range=100, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)        

    def setup_layout(self):
        # Sizer di base.
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Sizer per la gestione della sorgente dei dati.
        file_sizer = wx.BoxSizer(wx.VERTICAL)
        file_sizer.Add(self.file_button, 0, wx.ALL, 5)
        file_sizer.Add(self.file_path_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(file_sizer, 0, wx.ALL | wx.EXPAND, 10)

        # Sizer per la gestione della cartella di destinazione.
        folder_sizer = wx.BoxSizer(wx.VERTICAL)
        folder_sizer.Add(self.folder_button, 0, wx.ALL, 5)
        folder_sizer.Add(self.folder_path_label, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(folder_sizer, 0, wx.ALL | wx.EXPAND, 10)

        # Sizer per la gestione dell'inserimento del numero di esami da generare.
        main_sizer.Add(wx.StaticText(self.panel, label="Prefisso file:"), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.filename_text, 0, wx.ALL | wx.EXPAND, 5)
        
        # Sizer per la gestione dell'inserimento del numero di esami da generare.
        main_sizer.Add(wx.StaticText(self.panel, label="Materia"), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.materia_dropdown, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(wx.StaticText(self.panel, label="Classe:"), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.classe_dropdown, 0, wx.ALL | wx.EXPAND, 5)

        # Sizer per la gestione delle checkbox della scelta delle ere.
        main_sizer.Add(wx.StaticText(self.panel, label="Era:"), 0, wx.ALL | wx.EXPAND, 5)
        era_sizer = wx.BoxSizer(wx.HORIZONTAL)
        for checkbox in self.era_checkboxes:
            era_sizer.Add(checkbox, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(era_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # Sizer per la gestione dell'inserimento della tipologia delle domande.
        main_sizer.Add(wx.StaticText(self.panel, label="Tipologia:"), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.type_dropdown, 0, wx.ALL | wx.EXPAND, 5)

        # Sizer per la gestione dell'inserimento del numero di esami da generare e del numero di domande.
        main_sizer.Add(wx.StaticText(self.panel, label="Numero esami:"), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.exams_number, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(wx.StaticText(self.panel, label="Numero domande per esame:"), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.questions_number, 0, wx.ALL | wx.EXPAND, 5)

        # Sizer per la gestione delle opzioni di generazione degli esami.
        main_sizer.Add(wx.StaticText(self.panel, label="Opzioni:"), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.numera_domande_checkbox, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.mescola_domande_checkbox, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.mescola_opzioni_checkbox, 0, wx.ALL | wx.EXPAND, 5)

        # Sizer per la gestione del pulsante di avvio della generazione.
        main_sizer.Add(self.separator_line, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.start_button, 0, wx.ALL | wx.CENTRE, 5)

        # Sizer per la gestione dell'avamento della generazione.
        main_sizer.Add(self.progress_bar, 0, wx.ALL | wx.EXPAND, 5)

        self.panel.SetSizer(main_sizer)
        self.Fit()


    def on_choose_file(self, event):
        with wx.FileDialog(self, "Scegli la sorgente dati", wildcard="Tutti i file (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            file_path = file_dialog.GetPath()
            self.file_path_label.SetLabel(f"Path della sorgente: {file_path}")


    def on_choose_folder(self, event):
        with wx.DirDialog(self, "Scegli la destinazione degli esami", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as folder_dialog:
            if folder_dialog.ShowModal() == wx.ID_CANCEL:
                return
            folder_path = folder_dialog.GetPath()
            self.folder_path_label.SetLabel(f"Path della destinazione: {folder_path}")


    def on_start_button(self, event):
        self.start_button.Disable()
        self.progress_bar.Pulse()
        task_thread = BackgroundTaskThread(self)
        task_thread.start()


    def task_completed(self):
        self.progress_bar.SetValue(0)
        self.start_button.Enable()
        self.Layout()
        dlg = wx.MessageDialog(self, "Esami generati correttamente!", "COMPLETATO", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame(None, title="EXAMS GENERATOR")
    frame.Show()
    app.MainLoop()
