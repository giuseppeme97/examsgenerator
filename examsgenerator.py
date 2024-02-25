import pandas as pd
from exam import Exam
import random
import os

class ExamsGenerator():
    def __init__(self, config, logger=None) -> None:
        # Importazione della configurazione e del logger.
        self.config = config
        self.logger = logger

        # Caricamento della sorgente dati.
        self.load_source()
        
        if self.logger:
            self.logger.info("Sorgente caricata.")

    
    def update_config(self, config) -> None:
        self.config = config


    def load_source(self) -> None:
        _, ext = os.path.splitext(self.config["source_path"])
            
        # Viene caricata la sorgente dati, nel caso si tratti di un documento Excel.
        if ext in (".xlsx", ".xls"):
            self.df = pd.read_excel(self.config["source_path"])
        
        # Viene caricata la sorgente dati, nel caso si tratti di un documento CSV.
        elif ext == ".csv":
            self.df = pd.read_csv(self.config["source_path"],  sep=";")
        
        # Errore nel caricamento della sorgente dati.
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
                # Controlla se la materia dell'i-esima riga è quella scelta.
                row[self.config['subject_denomination']] == self.config['subject'] and

                # Controlla se la classe dell'i-esima riga è quella scelta.
                row[self.config['classroom_denomination']] == self.config['classroom'] and

                # Controlla se l'i-esima riga è da includere nelle domande degli esami.
                row[self.config['include_denomination']] == "SI"
            )
        else:
            return (
                # Controlla se la materia dell'i-esima riga è quella scelta.
                row[self.config['subject_denomination']] == self.config['subject'] and

                # Controlla se la classe dell'i-esima riga è quella scelta.
                row[self.config['classroom_denomination']] == self.config['classroom']
            )
            
    
    def pool_questions(self) -> None:
        # Viene inizializzato l'elenco delle domande da includere nell'i-esimo esame.
        self.questions = []
        
        # Vengono lette e filtrate le domande da includere nel pool di domande dell'i-esimo esame.
        for _, row in self.df.iterrows():
            
            # Viene effettuato il controllo sull'i-esima domanda.
            if (self.check_row(row)):
                
                # Viene costruita la struttura dati dell'i-esima domanda.
                # La chiave "question" ha attribuito come valore il testo della domanda.
                # La chiave "options" ha attributo come valore la lista delle opzioni di risposta.
                # Ogni opzione di risposta è un dizionario con chivi "text" e "correct".
                # La chiave "text" ha attribuito come valore il testo dell'opzione di risposta.
                # La chiave "correct" ha attributo come valore True se l'opzione di risposta è corretta, False altrimenti.
                question = {
                    "question": str(row[self.config['question_denomination']]),
                    "options": []
                }

                # Vengono aggiunte le strutture dati delle opzioni dell'i-esima domanda.
                for i in range(0, self.config['options_supported']):
                    question["options"].append({"text": str(row[f'{self.config["option_denomination"]}_{i + 1}']),
                                                "correct": True if int(row[self.config['solution_denomination']]) == (i + 1) else False})
                    
                # La domanda viene aggiunta al pool di domande dell'i-esimo esame
                self.questions.append(question)


    def shuffle_questions(self) -> list:
        # Se consentito nella configurazione, le domande del pool vengono mischiate.
        if self.config['shuffle_questions']:
            random.shuffle(self.questions)
        
        # Se consentito nella configurazione, le opzioni di risposta per ogni domanda vengono mischiate.
        if self.config['shuffle_options']:
            for question in self.questions:
                random.shuffle(question['options'])
        
        # Viene ricavato il numero di domande dal pool presente nella configurazione per ogni esame.
        return self.questions[0: self.config['questions_number']]


    def start(self) -> None:
        # Viene raccolto l'elenco delle domande da includere negli esami.
        self.pool_questions()

        # Vengono creati N istanze di esami diversi.
        for i in range(0, self.config["exams_number"]):
            # Vengono mescolate le domande all'interno del pool e ne viene ricavato un sottoinsieme.
            exam_questions = self.shuffle_questions()

            # Viene creata un'istanza di esame con le domande estratte.
            exam = Exam(self.config, exam_questions, i + 1, self.config["solutions"])
            
            # Genera ed esporta il documento Word dell'esame e, se indicato, il relativo correttore.
            exam.write()

            if self.logger:
                self.logger.info(f"Generato esame {i + 1}.")
            
            # Rimuove l'istanza dell'esame.
            del exam
