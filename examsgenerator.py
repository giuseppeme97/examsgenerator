import pandas as pd
from examwriter import ExamWriter
import random
import os

class ExamsGenerator():
    def __init__(self, config) -> None:
        self.config = config
        self.load_source()
        print("Sorgente caricata.")

    
    def update_config(self, config) -> None:
        self.config = config


    def load_source(self) -> None:
        _, ext = os.path.splitext(self.config["source_path"])
            
        if ext in (".xlsx", ".xls"):
            self.df = pd.read_excel(self.config["source_path"])
        elif ext == ".csv":
            self.df = pd.read_csv(self.config["source_path"],  sep=";")
        else:
            assert "Sorgente dati non corretta."


    def get_subjects(self) -> list:
        return sorted(pd.Series(self.df[self.config["subject_denomination"]].unique()).dropna().tolist()) 


    def get_classrooms(self) -> list:
        return sorted(list(map(int, pd.Series(self.df[self.config["classroom_denomination"]].unique()).dropna().tolist())))


    def get_rows(self) -> int:
        return self.df.shape[0]

    
    def check_row(self, row) -> bool:
        if self.config['inclusion']:
            return (
                row[self.config['subject_denomination']] == self.config['subject'] and
                row[self.config['classroom_denomination']] == self.config['classroom'] and
                row[self.config['include_denomination']] == "SI"
            )
        else:
            return (
                row[self.config['subject_denomination']] == self.config['subject'] and
                row[self.config['classroom_denomination']] == self.config['classroom']
            )
            
    
    def pool_questions(self) -> None:
        self.questions = []
        
        for _, row in self.df.iterrows():
            if (self.check_row(row)):
                question = {
                    "question": str(row[self.config['question_denomination']]),
                    "options": []
                }
                
                for i in range(0, self.config['options_supported']):
                    question["options"].append({"text": str(row[f'{self.config["option_denomination"]}_{i + 1}']),
                                                "correct": True if int(row[self.config['solution_denomination']]) == (i + 1) else False})
                
                self.questions.append(question)


    def shuffle_questions(self) -> list:
        if self.config['shuffle_questions']:
            random.shuffle(self.questions)
        
        if self.config['shuffle_options']:
            for question in self.questions:
                random.shuffle(question['options'])
        
        return self.questions[0: self.config['questions_number']]


    def start(self) -> None:
        self.pool_questions()

        for i in range(0, self.config["exams_number"]):
            exam_questions = self.shuffle_questions()
            exam = ExamWriter(self.config, exam_questions, i + 1)
            exam.write()            
            print(f"Generato esame {i + 1}.")
            del exam
