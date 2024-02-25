from examsgenerator import ExamsGenerator
import json

if __name__ == "__main__":
     with open("settings.json", 'r') as file:
          config = json.loads(file.read())

     generator = ExamsGenerator(config)
     generator.start()

