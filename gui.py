import tkinter as tk
from tkinter import filedialog

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaccia Tkinter")

        self.file_selection_frame = tk.LabelFrame(root, text="Selezione File", font=("Helvetica", 12))
        self.file_selection_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        # Pulsante per scegliere un file
        self.btn_choose_file = tk.Button(self.file_selection_frame, text="Scegli File", command=self.choose_file)
        self.btn_choose_file.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # Label per mostrare il path del file
        self.file_path_label = tk.Label(self.file_selection_frame, text="Path del file:")
        self.file_path_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        # Pulsante per scegliere una cartella
        self.btn_choose_folder = tk.Button(self.file_selection_frame, text="Scegli Cartella", command=self.choose_folder)
        self.btn_choose_folder.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        # Campo di testo per il nome del file
        self.file_name_entry = tk.Entry(self.file_selection_frame)
        self.file_name_entry.grid(row=3, column=0, padx=10, pady=5, sticky='w')

        # Menu a tendina per materia1
        self.materia1_var = tk.StringVar()
        self.materia1_menu = tk.OptionMenu(root, self.materia1_var, "materia1", "materia2", "materia3")
        self.materia1_menu.grid(row=4, column=0, padx=10, pady=5, sticky='w')

        # Menu a tendina per materia2
        self.materia2_var = tk.StringVar()
        self.materia2_menu = tk.OptionMenu(root, self.materia2_var, "materia1", "materia2", "materia3")
        self.materia2_menu.grid(row=5, column=0, padx=10, pady=5, sticky='w')

        # Checkbox per era1
        self.era1_var = tk.IntVar()
        self.era1_checkbox = tk.Checkbutton(root, text="Era 1", variable=self.era1_var)
        self.era1_checkbox.grid(row=6, column=0, padx=10, pady=5, sticky='w')

        # Checkbox per era2
        self.era2_var = tk.IntVar()
        self.era2_checkbox = tk.Checkbutton(root, text="Era 2", variable=self.era2_var)
        self.era2_checkbox.grid(row=7, column=0, padx=10, pady=5, sticky='w')

        # Checkbox per era3
        self.era3_var = tk.IntVar()
        self.era3_checkbox = tk.Checkbutton(root, text="Era 3", variable=self.era3_var)
        self.era3_checkbox.grid(row=8, column=0, padx=10, pady=5, sticky='w')

        # Menu a tendina per ok1
        self.ok1_var = tk.StringVar()
        self.ok1_menu = tk.OptionMenu(root, self.ok1_var, "ok1", "ok2")
        self.ok1_menu.grid(row=9, column=0, padx=10, pady=5, sticky='w')

        # Campo di input per numero intero maggiore di 1
        self.num1_entry = tk.Entry(root, validate="key", validatecommand=(root.register(self.validate_input), "%P"))
        self.num1_entry.grid(row=10, column=0, padx=10, pady=5, sticky='w')

        # Campo di input per numero intero maggiore di 1
        self.num2_entry = tk.Entry(root, validate="key", validatecommand=(root.register(self.validate_input), "%P"))
        self.num2_entry.grid(row=11, column=0, padx=10, pady=5, sticky='w')

        # Checkbox per Numera domande
        self.numera_domande_var = tk.IntVar()
        self.numera_domande_checkbox = tk.Checkbutton(root, text="Numera domande", variable=self.numera_domande_var)
        self.numera_domande_checkbox.grid(row=12, column=0, padx=10, pady=5, sticky='w')

        # Checkbox per Mescola domande
        self.mescola_domande_var = tk.IntVar()
        self.mescola_domande_checkbox = tk.Checkbutton(root, text="Mescola domande", variable=self.mescola_domande_var)
        self.mescola_domande_checkbox.grid(row=13, column=0, padx=10, pady=5, sticky='w')

        # Checkbox per Mescola opzioni
        self.mescola_opzioni_var = tk.IntVar()
        self.mescola_opzioni_checkbox = tk.Checkbutton(root, text="Mescola opzioni", variable=self.mescola_opzioni_var)
        self.mescola_opzioni_checkbox.grid(row=14, column=0, padx=10, pady=5, sticky='w')


    def choose_file(self):
        file_path = filedialog.askopenfilename()
        self.file_path_label.config(text=f"Path del file: {file_path}")

    def choose_folder(self):
        folder_path = filedialog.askdirectory()
        self.file_path_label.config(text=f"Path della cartella: {folder_path}")

    def validate_input(self, value):
        # Funzione di validazione per accettare solo numeri interi maggiori di 1
        try:
            if int(value) > 1:
                return True
            else:
                return False
        except ValueError:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
