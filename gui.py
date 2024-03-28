import wx
from examsgenerator import ExamsGenerator
import threading
import openpyxl
from openpyxl.styles import Side, Border
from settings import settings

class Task(threading.Thread):
    def __init__(self, parent_frame):
        threading.Thread.__init__(self)
        self.parent_frame = parent_frame
        self.daemon = True


    def run(self) -> None:
        try:
            self.parent_frame.generator.update_config(self.parent_frame.config)
            self.parent_frame.generator.start()
        except Exception as e:
            print(e)
            wx.CallAfter(self.parent_frame.task_error)
            return

        wx.CallAfter(self.parent_frame.task_completed)


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)
        self.panel = wx.Panel(self)
        self.create_widgets()
        self.setup_layout()
        self.SetSize((600, 820))
        self.config = settings
        

    def create_widgets(self) -> None:
        self.text_button_template = "Genera template sorgente domande"
        self.text_button_source = "File sorgente..."
        self.text_label_source_path = "Path della sorgente:"
        self.text_dialog_source = "Scegli la sorgente dati"
        self.text_button_destination = "Cartella destinazione..."
        self.text_label_dstination_path = "Path della destinazione:"
        self.text_dialog_destination = "Scegli la destinazione degli esami"
        self.text_checkbox_number_header = "Numera intestazione"
        self.text_checkbox_number_questions = "Numera domande"
        self.text_checkbox_shuffle_questions = "Mescola domande"
        self.text_checkbox_shuffle_options = "Mescola risposte"
        self.text_checkbox_solutions = "Esporta correttori"
        self.text_checkbox_inclusion = "Inclusione singola"
        self.text_prefix = "Prefisso file:"
        self.text_subject = "Materia:"
        self.text_classroom = "Classe:"
        self.text_header = "Intestazione:"
        self.text_exams_number = "Numero esami:"
        self.text_questions_number = "Numero domande per esame:"
        self.text_options = "Opzioni:"
        self.text_button_start = "Genera esami!"
        self.text_generation_error = ["Errore", "La generazione ha riscontrato un errore."]
        self.text_analysis_error = ["Errore", "Riscontrati problemi nell'analisi della sorgente dati."]
        self.text_analysis_complete = ["OK", "Sorgente caricata correttamente."]
        self.text_input_error = ["Attenzione", "Rivedere i campi inseriti e riprovare."]
        self.text_generation_complete = ["Completato", "Esami generati correttamente!"]
        self.subjects = []
        self.classrooms = []
        self.default_header = "Compito di ??? - Classe ?? - A.S. ????/????"
        self.default_exams_number = "5"
        self.default_questions_number = "30"
        self.source_path = None
        self.destination_path = None
        
        self.button_template = wx.Button(self.panel, label=self.text_button_template, style=wx.BU_LEFT)
        self.button_template.Bind(wx.EVT_BUTTON, self.export_template)

        self.button_source = wx.Button(self.panel, label=self.text_button_source, style=wx.BU_LEFT)
        self.button_source.Bind(wx.EVT_BUTTON, self.on_choose_file)
        self.label_source_path = wx.StaticText(self.panel, label=self.text_label_source_path)

        self.button_destination = wx.Button(self.panel, label=self.text_button_destination, style=wx.BU_LEFT)
        self.button_destination.Bind(wx.EVT_BUTTON, self.on_choose_folder)
        self.label_destination_path = wx.StaticText(self.panel, label=self.text_label_dstination_path)

        self.input_name = wx.TextCtrl(self.panel)
        self.input_name.SetHint("Prova Scritta Italiano")

        self.select_subject = wx.Choice(self.panel, choices=self.subjects)

        self.select_classroom = wx.Choice(self.panel, choices=self.classrooms)

        self.input_header = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER, value=self.default_header)

        self.input_exams_number = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER, value=self.default_exams_number)

        self.input_questions_number = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER, value=self.default_questions_number)

        self.checkbox_number_header = wx.CheckBox(self.panel, label=self.text_checkbox_number_header)
        self.checkbox_number_questions = wx.CheckBox(self.panel, label=self.text_checkbox_number_questions)
        self.checkbox_shuffle_questions = wx.CheckBox(self.panel, label=self.text_checkbox_shuffle_questions)
        self.checkbox_shuffle_options = wx.CheckBox(self.panel, label=self.text_checkbox_shuffle_options)
        self.checkbox_solutions = wx.CheckBox(self.panel, label=self.text_checkbox_solutions)
        self.checkbox_inclusion = wx.CheckBox(self.panel, label=self.text_checkbox_inclusion)

        self.separator = wx.StaticLine(self.panel, style=wx.LI_HORIZONTAL)
        
        self.button_start = wx.Button(self.panel, label=self.text_button_start, style=wx.BU_LEFT)
        self.button_start.Bind(wx.EVT_BUTTON, self.start)

        self.progress_bar = wx.Gauge(self.panel, range=100, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)     


    def setup_layout(self) -> None:
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        file_sizer = wx.BoxSizer(wx.VERTICAL)
        file_sizer.Add(self.button_template, 0, wx.ALL | wx.CENTRE, 5)
        file_sizer.Add(self.button_source, 0, wx.ALL, 5)
        file_sizer.Add(self.label_source_path, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(file_sizer, 0, wx.ALL | wx.EXPAND, 10)

        folder_sizer = wx.BoxSizer(wx.VERTICAL)
        folder_sizer.Add(self.button_destination, 0, wx.ALL, 5)
        folder_sizer.Add(self.label_destination_path, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(folder_sizer, 0, wx.ALL | wx.EXPAND, 10)

        main_sizer.Add(wx.StaticText(self.panel, label=self.text_prefix), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.input_name, 0, wx.ALL | wx.EXPAND, 5)
        
        main_sizer.Add(wx.StaticText(self.panel, label=self.text_subject), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.select_subject, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(wx.StaticText(self.panel, label=self.text_classroom), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.select_classroom, 0, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(wx.StaticText(self.panel, label=self.text_header), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.input_header, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(wx.StaticText(self.panel, label=self.text_exams_number), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.input_exams_number, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(wx.StaticText(self.panel, label=self.text_questions_number), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.input_questions_number, 0, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(wx.StaticText(self.panel, label=self.text_options), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.checkbox_number_header, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.checkbox_number_questions, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.checkbox_shuffle_questions, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.checkbox_shuffle_options, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.checkbox_solutions, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.checkbox_inclusion, 0, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(self.separator, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.button_start, 0, wx.ALL | wx.CENTRE, 5)

        main_sizer.Add(self.progress_bar, 0, wx.ALL | wx.EXPAND | wx.CENTRE, 5)

        self.panel.SetSizer(main_sizer)
        self.Fit()


    def analyze_source(self):
        self.config["source_path"] = self.source_path
        self.select_subject.Clear()
        self.select_classroom.Clear()
        
        try:
            self.generator = ExamsGenerator(self.config)
            self.select_subject.AppendItems(self.generator.get_subjects())
            self.select_classroom.AppendItems(list(map(str, self.generator.get_classrooms())))
            self.label_source_path.SetLabel(f"{self.text_label_source_path} {self.source_path}")
            self.show_dialog(self.text_analysis_complete[0], f"{self.text_analysis_complete[1]} Individuate {self.generator.get_rows()} domande.")
        except:
            self.source_path = ""
            self.show_dialog(self.text_analysis_error[0], self.text_analysis_error[1])


    def export_template(self, event):
        with wx.DirDialog(self, self.text_dialog_destination, style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as folder_dialog:
            if folder_dialog.ShowModal() == wx.ID_CANCEL:
                return
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            headers = [
                self.config["subject_denomination"], 
                self.config["classroom_denomination"], 
                self.config["include_denomination"], 
                self.config["question_denomination"], 
                self.config["solution_denomination"], 
                f"{self.config['option_denomination']}_1",
                f"{self.config['option_denomination']}_2",
                f"{self.config['option_denomination']}_3",
                f"{self.config['option_denomination']}_4"]
            for col_num, header in enumerate(headers, 1):
                cell = sheet.cell(row=1, column=col_num, value=header)
                cell.border = Border(bottom=Side(style='thin', color='000000'))                
            workbook.save(f"{folder_dialog.GetPath()}/template.xlsx")


    def on_choose_file(self, event) -> None:
        with wx.FileDialog(self, self.text_dialog_source, wildcard="Tutti i file (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            self.source_path = file_dialog.GetPath()
            self.analyze_source()
            self.label_source_path.SetLabel(f"{self.text_label_source_path} {self.source_path}")


    def on_choose_folder(self, event) -> None:
        with wx.DirDialog(self, self.text_dialog_destination, style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as folder_dialog:
            if folder_dialog.ShowModal() == wx.ID_CANCEL:
                return
            self.destination_path = folder_dialog.GetPath()
            self.label_destination_path.SetLabel(f"{self.text_label_dstination_path} {self.destination_path}")


    def build_config(self) -> bool:
        confirm = (
                (self.source_path is not None and self.source_path != "") and 
                (self.destination_path is not None and self.destination_path != "") and
                (self.input_name.GetValue() is not None and self.input_name.GetValue() != "") and
                (self.select_subject.GetStringSelection() is not None and self.select_subject.GetStringSelection() != "") and
                (self.select_classroom.GetStringSelection() is not None and self.select_classroom.GetStringSelection() != "" and self.select_classroom.GetStringSelection().isnumeric()) and
                (self.input_header.GetValue() is not None and self.input_header.GetValue() != "") and
                (self.input_exams_number.GetValue() is not None and self.input_exams_number.GetValue() != "" and self.input_exams_number.GetValue().isnumeric()) and
                (self.input_questions_number.GetValue() is not None and self.input_questions_number.GetValue() != "" and self.input_questions_number.GetValue().isnumeric())
        )

        if confirm:
            self.config["source_path"] = self.source_path
            self.config["destination_path"] = self.destination_path
            self.config["file_name"] = self.input_name.GetValue()
            self.config["subject"] = self.select_subject.GetStringSelection().upper()
            self.config["classroom"] = int(self.select_classroom.GetStringSelection())
            self.config["title"] = self.input_header.GetValue()
            self.config["exams_number"] = int(self.input_exams_number.GetValue())
            self.config["questions_number"] = int(self.input_questions_number.GetValue())
            self.config["number_heading"] = self.checkbox_number_header.GetValue()
            self.config["number_questions"] = self.checkbox_number_questions.GetValue()
            self.config["shuffle_questions"] = self.checkbox_shuffle_questions.GetValue()
            self.config["shuffle_options"] = self.checkbox_shuffle_options.GetValue()
            self.config["solutions"] = self.checkbox_solutions.GetValue()
            self.config["inclusion"] = self.checkbox_inclusion.GetValue()
        return confirm


    def start(self, event) -> None:
        if self.build_config():
            self.start_progress()
            task_thread = Task(self)
            task_thread.start()
        else:
            self.show_dialog(self.text_input_error[0], self.text_input_error[1])


    def task_error(self) -> None:
        self.stop_progress()
        self.show_dialog(self.text_generation_error[0], self.text_generation_error[1])


    def task_completed(self) -> None:
        self.stop_progress()
        self.show_dialog(self.text_generation_complete[0], self.text_generation_complete[1])


    def show_dialog(self, title, message) -> None:
        dlg = wx.MessageDialog(self, message, title, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    
    def start_progress(self) -> None:
        self.button_start.Disable()
        self.progress_bar.Pulse()
        self.Layout()

    
    def stop_progress(self) -> None:
        self.progress_bar.SetValue(0)
        self.button_start.Enable()
        self.Layout()



if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame(None, title="Exams Generator")
    frame.Show()
    app.MainLoop()
