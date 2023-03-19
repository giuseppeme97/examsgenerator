from examsgenerator import ExamsGenerator

config = {
    "same_folder": True,
    "source_path": None,
    "source_file": "Domande",
    "source_extension": ".xlsx",
    "destination_file": "exam",
    "destination_folder": None,
    "subject": "TPSIT",
    "classroom": "4H",
    "era": [1],
    "sector": "TEORIA",
    "title": "Compito di T.P.S.I.T. - A.S. 2022/2023 - Classe 4H",
    "heading": "Cognome e Nome: ___________________________________________",
    "questions_number": 21,
    "options_supported": 4,
    "shuffle_questions": True,
    "shuffle_options": True,
    "exams_number": 5,
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

if __name__ == "__main__":
    exams_generator = ExamsGenerator(config)
    exams_generator.start()

