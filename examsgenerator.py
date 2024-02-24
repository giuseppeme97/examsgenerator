import pandas as pd
from exam import Exam
import random


class ExamsGenerator():
    def __init__(self, config, logger=None) -> None:
        # Importazione della configurazione e del logger.
        self.config = config
        self.logger = logger

        # Caricamento della sorgente dati.
        # La sorgente dati può essere presente nella stessa directory dello script.
        if self.config["same_folder"]:
            self.df = self.get_dataframe(f"{self.config['source_file']}{self.config['source_extension']}")
        
        # La sorgente dati può essere caricata da un path specifico.
        else:
            self.df = self.get_dataframe(self.config["source_path"])
        
        if self.logger:
            self.logger.info("Sorgente caricata.")

        # Avvia la generazione.
        self.start()


    def get_dataframe(self, path) -> object:
        # Viene caricata la sorgente dati, nel caso si tratti di un documento Excel.
        if self.config["source_extension"] == ".xlsx" or self.config["source_extension"] == ".xls":
            return pd.read_excel(path)
        
        # Viene caricata la sorgente dati, nel caso si tratti di un documento CSV.
        elif self.config["source_extension"] == ".csv":
            return pd.read_csv(path,  sep=";")
        
        # Errore nel caricamento della sorgente dati.
        else:
            assert "Sorgente dati non corretta."

    
    def check_row(self, row) -> bool:
        return (
            # Controlla se la materia dell'i-esima riga è quella scelta.
            row[self.config['subject_denomination']] == self.config['subject'] and

            # Controlla se la classe dell'i-esima riga è quella scelta.
            row[self.config['classroom_denomination']] == self.config['classroom'] and

            # Controlla se l'era dell'i-esima riga è quella scelta.
            row[self.config['era_denomination']] in self.config['era'] and

            # Controlla se il settore dell'i-esima riga è quella scelto.
            row[self.config['sector_denomination']] == self.config['sector'] and

            # Controlla se l'i-esima riga è da includere nelle domande degli esami.
            row[self.config['include_denomination']] == "SI"
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
            exam = Exam(self.config, exam_questions)
            
            # Genera ed esporta il documento Word dell'esame e il relativo correttore.
            exam.write(i)

            if self.logger:
                self.logger.info(f"Generato esame {i + 1}.")
            
            # Rimuove l'istanza dell'esame.
            del exam
