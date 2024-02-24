import wx
import threading
import time

class BackgroundTaskThread(threading.Thread):
    def __init__(self, parent_frame):
        threading.Thread.__init__(self)
        self.parent_frame = parent_frame
        self.daemon = True


    def run(self):
        # ******************* #
        # ********TASK******* #
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
        self.text_button_source = "File sorgente..."
        self.text_label_source_path = "Path della sorgente:"
        self.text_dialog_source = "Scegli la sorgente dati"
        self.text_button_destination = "Cartella destinazione..."
        self.text_label_dstination_path = "Path della destinazione:"
        self.text_dialog_destination = "Scegli la destinazione degli esami"
        self.text_checkbox_era = "Era"
        self.text_checkbox_numeration = "Numera domande"
        self.text_checkbox_shuffle_questions = "Mescola domande"
        self.text_checkbox_shuffle_options = "Mescola opzioni"
        self.text_prefix = "Prefisso file:"
        self.text_subject = "Materia:"
        self.text_classroom = "Classe:"
        self.text_era = "Era:"
        self.text_type = "Tipologia:"
        self.text_header = "Intestazione:"
        self.text_exams_number = "Numero esami:"
        self.text_questions_number = "Numero domande per esame:"
        self.text_options = "Opzioni:"
        self.text_button_start = "Genera!"
        self.text_complete = ["COMPLETATO", "Esami generati correttamente!"]
        self.subjects = ["Sistemi e Reti", "TPSIT", "Informatica"]
        self.classrooms = ["3", "4", "5"]
        self.types = ["Teoria", "Pratico"]
        self.default_header = "Compito di Sistemi e Reti - A.S. 2023/2024 - Classe 3F"
        self.default_exams_number = "5"
        self.default_questions_number = "30"

        # Pulsante per la selezione della sorgente dati.
        self.button_source = wx.Button(self.panel, label=self.text_button_source, style=wx.BU_LEFT)
        self.button_source.Bind(wx.EVT_BUTTON, self.on_choose_file)
        self.label_source_path = wx.StaticText(self.panel, label=self.text_label_source_path)

        # Pulsante per la selezione della destinazione degli esami.
        self.button_destination = wx.Button(self.panel, label=self.text_button_destination, style=wx.BU_LEFT)
        self.button_destination.Bind(wx.EVT_BUTTON, self.on_choose_folder)
        self.label_dstination_path = wx.StaticText(self.panel, label=self.text_label_dstination_path)

        # Input per l'inserimento dei nomi degli esami.
        self.input_name = wx.TextCtrl(self.panel)

        # Selection per la scelta della materia.
        self.select_subject = wx.Choice(self.panel, choices=self.subjects)

        # Selection per la scelta della classe.
        self.select_classroom = wx.Choice(self.panel, choices=self.classrooms)

        # Checkboxs per la scelta delle ere.
        self.checkbox_era = [wx.CheckBox(self.panel, label=f"{self.text_checkbox_era} {i}") for i in range(1, 4)]

        # Selection per la scelta del tipo di domande.
        self.select_type = wx.Choice(self.panel, choices=self.types)

        # Input per l'inserimento dell'intestazione dell'esame.
        self.input_header = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER, value=self.default_header)

        # Input per l'inserimento del numero di esami da generare.
        self.input_exams_number = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER, value=self.default_exams_number)

        # Input per l'inserimento del numero di domande da inserire in ogni esame.
        self.input_questions_number = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER, value=self.default_questions_number)

        # Checkbox per le opzioni di generazione degli esami.
        self.checkbox_numeration = wx.CheckBox(self.panel, label=self.text_checkbox_numeration)
        self.checkbox_shuffle_questions = wx.CheckBox(self.panel, label=self.text_checkbox_shuffle_questions)
        self.checkbox_shuffle_options = wx.CheckBox(self.panel, label=self.text_checkbox_shuffle_options)

        # Linea di separazione.
        self.separator = wx.StaticLine(self.panel, style=wx.LI_HORIZONTAL)
        
        # Pulsante per avviare la generazione degli esami.
        self.button_start = wx.Button(self.panel, label=self.text_button_start, style=wx.BU_LEFT)
        self.button_start.Bind(wx.EVT_BUTTON, self.on_start_button)

        # Barra di avanzamento.
        self.progress_bar = wx.Gauge(self.panel, range=100, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)        

    def setup_layout(self):
        # Sizer di base.
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Sizer per la gestione della sorgente dei dati.
        file_sizer = wx.BoxSizer(wx.VERTICAL)
        file_sizer.Add(self.button_source, 0, wx.ALL, 5)
        file_sizer.Add(self.label_source_path, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(file_sizer, 0, wx.ALL | wx.EXPAND, 10)

        # Sizer per la gestione della cartella di destinazione.
        folder_sizer = wx.BoxSizer(wx.VERTICAL)
        folder_sizer.Add(self.button_destination, 0, wx.ALL, 5)
        folder_sizer.Add(self.label_dstination_path, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(folder_sizer, 0, wx.ALL | wx.EXPAND, 10)

        # Sizer per la gestione dell'inserimento del numero di esami da generare.
        main_sizer.Add(wx.StaticText(self.panel, label=self.text_prefix), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.input_name, 0, wx.ALL | wx.EXPAND, 5)
        
        # Sizer per la gestione dell'inserimento del numero di esami da generare.
        main_sizer.Add(wx.StaticText(self.panel, label=self.text_subject), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.select_subject, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(wx.StaticText(self.panel, label=self.text_classroom), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.select_classroom, 0, wx.ALL | wx.EXPAND, 5)

        # Sizer per la gestione delle checkbox della scelta delle ere.
        main_sizer.Add(wx.StaticText(self.panel, label=self.text_era), 0, wx.ALL | wx.EXPAND, 5)
        era_sizer = wx.BoxSizer(wx.HORIZONTAL)
        for checkbox in self.checkbox_era:
            era_sizer.Add(checkbox, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(era_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # Sizer per la gestione dell'inserimento della tipologia delle domande.
        main_sizer.Add(wx.StaticText(self.panel, label=self.text_type), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.select_type, 0, wx.ALL | wx.EXPAND, 5)

        # Sizer per la gestione dell'inserimento del numero di esami da generare e del numero di domande.
        main_sizer.Add(wx.StaticText(self.panel, label=self.text_header), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.input_header, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(wx.StaticText(self.panel, label=self.text_exams_number), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.input_exams_number, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(wx.StaticText(self.panel, label=self.text_questions_number), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.input_questions_number, 0, wx.ALL | wx.EXPAND, 5)

        # Sizer per la gestione delle opzioni di generazione degli esami.
        main_sizer.Add(wx.StaticText(self.panel, label=self.text_options), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.checkbox_numeration, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.checkbox_shuffle_questions, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.checkbox_shuffle_options, 0, wx.ALL | wx.EXPAND, 5)

        # Sizer per la gestione del pulsante di avvio della generazione.
        main_sizer.Add(self.separator, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.button_start, 0, wx.ALL | wx.CENTRE, 5)

        # Sizer per la gestione dell'avamento della generazione.
        main_sizer.Add(self.progress_bar, 0, wx.ALL | wx.EXPAND, 5)

        self.panel.SetSizer(main_sizer)
        self.Fit()


    def on_choose_file(self, event):
        with wx.FileDialog(self, self.text_dialog_source, wildcard="Tutti i file (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            file_path = file_dialog.GetPath()
            self.label_source_path.SetLabel(f"{self.text_label_source_path} {file_path}")


    def on_choose_folder(self, event):
        with wx.DirDialog(self, self.text_dialog_destination, style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as folder_dialog:
            if folder_dialog.ShowModal() == wx.ID_CANCEL:
                return
            folder_path = folder_dialog.GetPath()
            self.label_dstination_path.SetLabel(f"{self.text_label_dstination_path} {folder_path}")


    def build_config(self):
        pass


    def on_start_button(self, event):
        self.button_start.Disable()
        self.progress_bar.Pulse()
        task_thread = BackgroundTaskThread(self)
        task_thread.start()


    def task_completed(self):
        self.progress_bar.SetValue(0)
        self.button_start.Enable()
        self.Layout()
        dlg = wx.MessageDialog(self, self.text_complete[1], self.text_complete[0], wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame(None, title="Exams Generator")
    frame.Show()
    app.MainLoop()
