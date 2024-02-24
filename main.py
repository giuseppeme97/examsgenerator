from examsgenerator import ExamsGenerator
import json
import logging
from colorama import init, Fore, Style

if __name__ == "__main__":
     # Viene letto il JSON con la configurazione da importare.
     with open("settings.json", 'r') as j:
          config = json.loads(j.read())

     # Viene istanziato e configurato il logger.
     init(autoreset=True)
     logger = logging.getLogger(__name__)
     console_handler = logging.StreamHandler()
     formatter = logging.Formatter(f"{Style.BRIGHT}{Fore.GREEN}%s{Style.RESET_ALL}" % "%(message)s")
     console_handler.setFormatter(formatter)
     logger.addHandler(console_handler)
     logger.setLevel(logging.INFO)
     
     # Viene istanziato e avviato il generatore con la configurazione passata.
     _ = ExamsGenerator(config, logger=logger)

