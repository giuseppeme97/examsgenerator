from examsgenerator import ExamsGenerator
import json

# Viene letto il JSON con la configurazione da importare.
with open("settings.json", 'r') as j:
     config = json.loads(j.read())

# Viene avviato il generatore.
exams_generator = ExamsGenerator(config)
exams_generator.start()    


