import sys
from PySide6.QtWidgets import QWidget, QMessageBox, QFrame, QLineEdit, QSpinBox, QVBoxLayout, QHBoxLayout, QApplication, QGridLayout, QComboBox, QMainWindow, QPushButton, QCheckBox, QLabel, QProgressBar, QFileDialog
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from examsgenerator import ExamsGenerator
import os


class MyThread(QThread):
    progress_update = pyqtSignal(int)

    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        config = {
            "same_folder": False,
            "source_path": self.config["choosed_file"],
            "source_file": None,
            "source_extension": self.config["extension"],
            "destination_file": "exam",
            "destination_folder": self.config["choosed_folder"],
            "subject": self.config["subject"],
            "classroom": self.config["classroom"],
            "era": self.config["era"],
            "sector": self.config["sector"],
            "title": self.config["title"],
            "heading": "Cognome e Nome: ___________________________________________",
            "questions_number": self.config["questions_number"],
            "options_supported": 4,
            "shuffle_questions": self.config["shuffle_questions"],
            "shuffle_options": self.config["shuffle_options"],
            "exams_number": self.config["exams_number"],
            "subject_denomination": "MATERIA",
            "classroom_denomination": "CLASSE",
            "era_denomination": "ERA",
            "sector_denomination": "SETTORE",
            "type_denomination": "TIPO",
            "question_denomination": "DOMANDA",
            "solution_denomination": "CORRETTA",
            "option_denomination": "OPZIONE",
            "include_denomination": "INCLUDERE"
        }
        exams_generator = ExamsGenerator(config)
        exams_generator.start()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exams Generator")
        main_layout = QVBoxLayout()

        self.button_file = QPushButton("File domande...", self)
        self.button_file.clicked.connect(self.choose_file)
        main_layout.addWidget(self.button_file)

        self.choosed_file = QLabel("", self)
        self.choosed_file.hide()
        main_layout.addWidget(self.choosed_file)

        self.button_folder = QPushButton("Cartella esami...", self)
        self.button_folder.clicked.connect(self.choose_folder)
        main_layout.addWidget(self.button_folder)

        self.choosed_folder = QLabel("", self)
        self.choosed_folder.hide()
        main_layout.addWidget(self.choosed_folder)

        hline1 = QFrame()
        hline1.setFrameShape(QFrame.HLine)
        hline1.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(hline1)

        self.subject = QComboBox()
        self.subject.addItem("SISTEMI E RETI - 3F")
        self.subject.addItem("SISTEMI E RETI - 4F")
        self.subject.addItem("SISTEMI E RETI - 5F")
        self.subject.addItem("TPSIT - 3H")
        self.subject.addItem("TPSIT - 4H")
        main_layout.addWidget(self.subject)

        self.sector = QComboBox()
        self.sector.addItem("TEORIA")
        self.sector.addItem("PRATICA")
        main_layout.addWidget(self.sector)

        era_layout = QHBoxLayout()
        self.era1 = QCheckBox("Tr 1", self)
        self.era1.setChecked(True)
        era_layout.addWidget(self.era1)
        self.era2 = QCheckBox("Tr 2", self)
        self.era2.setChecked(True)
        era_layout.addWidget(self.era2)
        self.era3 = QCheckBox("Tr 3", self)
        self.era3.setChecked(True)
        era_layout.addWidget(self.era3)
        main_layout.addLayout(era_layout)

        hline3 = QFrame()
        hline3.setFrameShape(QFrame.HLine)
        hline3.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(hline3)

        self.shuffle_questions = QCheckBox("Mescola domande", self)
        self.shuffle_questions.setChecked(True)
        main_layout.addWidget(self.shuffle_questions)

        self.shuffle_options = QCheckBox("Mescola opzioni", self)
        self.shuffle_options.setChecked(True)
        main_layout.addWidget(self.shuffle_options)

        hline2 = QFrame()
        hline2.setFrameShape(QFrame.HLine)
        hline2.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(hline2)

        self.h_title = QLabel("Titolo esame:", self)
        main_layout.addWidget(self.h_title)
        self.title = QLineEdit()
        self.title.setPlaceholderText("Aggiungi titolo esame...")
        main_layout.addWidget(self.title)

        self.h_exams_number = QLabel("Numero esami:", self)
        main_layout.addWidget(self.h_exams_number)
        self.exams_number = QSpinBox()
        self.exams_number.setMinimum(1)
        self.exams_number.setMaximum(100)
        main_layout.addWidget(self.exams_number)

        self.h_questions_number = QLabel("Numero domande:", self)
        main_layout.addWidget(self.h_questions_number)
        self.questions_number = QSpinBox()
        self.questions_number.setMinimum(1)
        self.questions_number.setMaximum(100)
        main_layout.addWidget(self.questions_number)

        self.button_start = QPushButton("Genera esami!", self)
        self.button_start.clicked.connect(self.start_stop_task)
        main_layout.addWidget(self.button_start)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.hide()
        self.progress_bar.setMaximum(0)
        main_layout.addWidget(self.progress_bar)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        self.thread = None

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Seleziona cartella')
        if folder:
            self.choosed_folder.setText(str(folder))
            self.choosed_folder.show()

    def choose_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Seleziona file", "", "Excel e CSV Files (*.xlsx *.xls *.csv)")
        if file_name:
            self.extension = os.path.splitext(file_name)[1]
            self.choosed_file.setText(str(file_name))
            self.choosed_file.show()

    def show_alert(self, message):
        msg = QMessageBox()
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    def start_stop_task(self):
        if self.thread is None:
            self.progress_bar.show()
            self.button_start.setEnabled(False)
            config = {
                "choosed_file": self.choosed_file.text(),
                "extension": self.extension,
                "choosed_folder": self.choosed_folder.text(),
                "subject": self.subject.currentText().split(" - ")[0],
                "classroom": self.subject.currentText().split(" - ")[1],
                "era": [1 if self.era1.isChecked() else None, 2 if self.era2.isChecked() else None, 3 if self.era3.isChecked() else None],
                "sector": self.sector.currentText(),
                "title": self.title.text(),
                "questions_number": self.questions_number.value(),
                "shuffle_questions": self.shuffle_questions.isChecked(),
                "shuffle_options": self.shuffle_options.isChecked(),
                "exams_number": self.exams_number.value()
            }
            self.thread = MyThread(config)
            self.thread.start()
        else:
            self.thread.requestInterruption()
            self.button_start.setEnabled(False)
        self.thread.finished.connect(self.reset_task)

    def reset_task(self):
        self.progress_bar.hide()
        self.button_start.setEnabled(True)
        self.thread = None
        self.show_alert("Esami generati!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
