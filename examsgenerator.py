import pandas as pd
from utility import *
from exam import Exam


class ExamsGenerator():
    def __init__(self, config) -> None:
        self.config = config
        if self.config["same_folder"]:
            self.df = self.get_dataframe(
                f"{self.config['source_file']}{self.config['source_extension']}")
        else:
            self.df = self.get_dataframe(self.config["source_path"])
        self.show_params()

    def get_dataframe(self, path):
        if self.config["source_extension"] == ".xlsx" or self.config["source_extension"] == ".xls":
            return pd.read_excel(path)
        elif self.config["source_extension"] == ".csv":
            print(path)
            return pd.read_csv(path,  sep=";")
        else:
            return None

    def show_params(self) -> None:
        print("********************")
        print(f"Materia: {self.config['subject']}")
        print(f"Classe: {self.config['classroom']}")
        print("********************")

    def check_row(self, row) -> bool:
        return (
            row[self.config['subject_denomination']] == self.config['subject'] and
            row[self.config['classroom_denomination']] == self.config['classroom'] and
            row[self.config['era_denomination']] in self.config['era'] and
            row[self.config['sector_denomination']] == self.config['sector'] and
            row[self.config['include_denomination']] == "SI"
        )

    def pool_questions(self) -> None:
        self.questions = []
        for _, row in self.df.iterrows():
            if (self.check_row(row)):
                question = {
                    "question": str(row[self.config['question_denomination']]),
                    "type": row[self.config['type_denomination']],
                    "options": []
                }
                if row[self.config['type_denomination']] == "QUIZ":
                    for i in range(0, self.config['options_supported']):
                        question["options"].append({"text": str(row[f'{self.config["option_denomination"]}_{i + 1}']),
                                                   "correct": True if int(row[self.config['solution_denomination']]) == (i + 1) else False})
                self.questions.append(question)
            #print(row[self.config['question_denomination']])

    def start(self) -> None:
        self.pool_questions()
        for i in range(0, self.config["exams_number"]):
            exam = Exam(self.config, self.questions)
            exam.shuffle_questions()
            exam.write_exam(i)
            exam.write_exam_with_solutions(i)
            del exam
        print("Esami generati!")
        print("********************")
