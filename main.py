from examsgenerator import ExamsGenerator
import json

with open("settings.json", 'r') as j:
     config = json.loads(j.read())

if __name__ == "__main__":
    exams_generator = ExamsGenerator(config)
    exams_generator.start()


