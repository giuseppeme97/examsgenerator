from examsgenerator import ExamsGenerator
import json

if __name__ == "__main__":
     with open("settings.json", 'r') as j:
          config = json.loads(j.read())

     generator = ExamsGenerator(config)
     generator.start()

