from tkinter import ttk
from matplotlib.figure import Figure
import tkinter as tk
import os
import topsis
import visuals
import pandas as pd
import etl
import comparison
import glob
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Gui:
    functionalities = sorted(['Utwórz wizualizację', 'Utwórz ranking',
                             'Porównaj obszary', 'Pobierz zestaw danych'])

    def __init__(self):
        self.loaded_graph = False
        self.graph = None
        self.canvas = None
        self.ax = None
        self.variables_details = dict(zip(pd.read_excel('details_variables.xlsx')['name'],
                                          pd.read_excel('details_variables.xlsx', dtype={'id_x': str})['id_x']))
        self.voivodeships_poland = dict(pd.read_excel('voivodeships_poland.xlsx',
                                                      dtype={'id': str})[['id', 'name']].values).values()

    def choose_functionality(self, option, window):
        match option:
            case 'Pobierz zestaw danych':
                try:
                    etl.get_dataset().to_excel(r'gus.xlsx')
                    self.create_message_window()
                except Exception as err:
                    self.create_message_window(message=f"{str(type(err)).capitalize()}: {err}")
            case 'Porównaj obszary':
                window.destroy()
                comparison.compare()
            case 'Utwórz wizualizację':
                window.destroy()
                self.create_window_for_visuals()
            case 'Utwórz ranking':
                window.destroy()
                topsis.create_ranking()
            case 'Sprawdź zależność zmiennych':
                window.destroy()
                self.create_window_for_visuals()
            case _:
                print("inne...")

    def create_message_window(self, message='Sukces'):
        """
        Funkcja wyświeta okienko powiadamiające użytkownika o sukcesie pobrania pliku.
        """
        root = tk.Tk()
        height = 100
        width = 450
        root.geometry(f"{width}x{height}")
        center_x = int((root.winfo_screenwidth() - width) / 2)
        center_y = int((root.winfo_screenheight() - height) / 2)
        root.geometry(f"+{center_x}+{center_y}")
        root.title("Powiadomienie")
        success_label = tk.Label(root, text=message)
        success_label.pack(expand=True)
        #root.after(3000, root.destroy)
        root.mainloop()

    def start_program(self):
        window = tk.Tk()
        # Displaying window at the center of a screen
        height = 200
        width = 450
        window.geometry(f"{width}x{height}")
        center_x = int((window.winfo_screenwidth() - width) / 2)
        center_y = int((window.winfo_screenheight() - height) / 2)
        window.geometry(f"+{center_x}+{center_y}")
        window.title("Menu")
        # Adding buttons for every available function
        for function in self.functionalities:
            button = tk.Button(window,
                               text=function,
                               command=lambda option=function: self.choose_functionality(option, window))
            button.pack(pady=5)
        window.mainloop()

    def create_window_for_visuals(self):
        """
        Funkcja tworzy okno do generowania wykresów punktowych i map.
        """
        # Inicjalizacja głównego okna Tkinter
        root = tk.Tk()
        root.title('Wykresy')

        # Ustawienia rozmiaru i położenia okna
        height = 600
        width = 1720
        root.geometry(f"{width}x{height}")
        center_x = int((root.winfo_screenwidth() - width) / 2)
        center_y = int((root.winfo_screenheight() - height) / 2)
        root.geometry(f"+{center_x}+{center_y}")

        # Odczyt nazw zmiennych dostępnych do wuzualizacji z pliku Excel
        col_names = list(self.variables_details.keys())


        def update_ui(*args):
            """
            Funkcja do aktualizacji interfejsu użytkownika w zależności od wybranej wartości w dropdownie.
            """

            selected_value = dropdown1.get()
            label_column_name.grid(row=1, column=0, pady=5, sticky=tk.W)
            if selected_value in ["Wykres punktowy", 'Heatmap']:
                dropdown2.grid()
                dropdown3.grid()
            else:
                dropdown2.grid()
                dropdown3.grid_remove()

            if selected_value in ["Dendogram"]:
                dropdown2.grid_remove()
                dropdown3.grid_remove()
                label_column_name.grid_remove()


            if selected_value == "Wykres kołowy":
                dropdown2['values'] = [col_names[0], col_names[1], col_names[2], col_names[6], col_names[7],
                                  col_names[8], col_names[10], col_names[15]]
            else:
                dropdown2['values'] = col_names

        # Ramka po lewej stronie przeznaczona na liste opcji i przyciski
        left_frame = ttk.Frame(root, padding=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # Listy opcji
        ttk.Label(left_frame, text="Typ wykresu:").grid(row=0, column=0, pady=5, sticky=tk.W)
        dropdown1_var = tk.StringVar()
        dropdown1 = ttk.Combobox(left_frame, values=sorted(['Dendogram', 'Mapa', 'Wykres punktowy', 'Wykres kolumnowy', 'Wykres kołowy', 'Heatmap']), state="readonly",
                                 textvariable=dropdown1_var, width=40)
        dropdown1_var.set('Mapa')
        dropdown1.grid(row=0, column=1, pady=5, padx=(0, 10))
        dropdown1_var.trace_add("write", update_ui)

        label_column_name = ttk.Label(left_frame, text="Nazwa kolumn(y):")
        label_column_name.grid(row=1, column=0, pady=5, sticky=tk.W)

        dropdown2 = ttk.Combobox(left_frame, values=col_names, state="readonly", width=40)
        dropdown2.set(col_names[0])
        dropdown2.grid(row=1, column=1, pady=5, padx=(0, 10))

        dropdown3 = ttk.Combobox(left_frame, values=col_names, state="readonly", width=40)
        dropdown3.set(col_names[1])
        dropdown3.grid(row=2, column=1, pady=5, padx=(0, 10))
        dropdown3.grid_remove()

        # Ramka po prawej stronie przeznaczona na wykres
        right_frame = ttk.Frame(root)
        right_frame.grid(row=0, column=1, sticky="nsew")

        # Pusty wykres wyświetlany na początku
        self.graph = Figure(figsize=(5, 4), dpi=100, facecolor='none')
        self.ax = self.graph.add_subplot(111, facecolor='none')
        self.canvas = FigureCanvasTkAgg(self.graph, master=right_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        def save_as_pdf():
            """
            Funkcja zapisuje wykres jako plik PDF. Sparwdza czy typ danego wykresu już został zapisany.
            Jeżeli tak to pobiera największy numer wykresu.
            """
            numer = 1
            wykres = dropdown1.get().replace(' ', '_')
            pdf_files = glob.glob('*.pdf')
            numery_plikow = []
            for pdf in pdf_files:
                if wykres in pdf:
                    try:
                        numery_plikow.append(int(pdf.split('_')[-1].split('.')[0]))
                    except Exception as err:
                        self.create_message_window(message=f"{str(type(err)).capitalize()}: {err}.\nProszę zmienić lokalizację pliku, którego nazwa została zmodyfikowana.")
            if numery_plikow:
                numer = max(numery_plikow) + 1
            file_path = (f'{dropdown1.get()}_{numer}.pdf'
                         .replace(' ', '_'))
            self.graph.savefig(file_path, format='pdf')

        def generate_plot():
            """
            Funkcja generuje wykres na podstawie wybranych opcji.
            """
            col_1 = dropdown2.get()
            chart_type = dropdown1.get()
            try:
                if chart_type == 'Heatmap':
                    col_2 = dropdown3.get()
                    self.graph = visuals.create_heatmap(
                        name_1=dropdown2.get(), name_2=col_2,
                        id_1=self.variables_details[col_1], id_2=self.variables_details[col_2]
                    )
                elif chart_type == 'Wykres punktowy':
                    col_2 = dropdown3.get()
                    if col_2 == '':
                        self.create_message_window('Uzupełnij nazwę kolumny')
                    self.graph = visuals.create_scatter_plot(
                        name_1=col_1, name_2=col_2,
                        id_1=self.variables_details[col_1], id_2=self.variables_details[col_2]
                    )
                elif chart_type == 'Mapa':
                    self.graph = visuals.create_map(
                        name_1=col_1, id_1=self.variables_details[col_1]
                    )
                elif chart_type == 'Dendogram':
                    self.graph = visuals.create_dendrogram()
                elif chart_type == 'Wykres kolumnowy':
                   self.graph = visuals.create_bargraph(
                        name_1=col_1, id_1=self.variables_details[col_1]
                    )
                elif chart_type == 'Wykres kołowy':
                   self.graph = visuals.create_piechart(
                        name_1=col_1, id_1=self.variables_details[col_1]
                    )

                self.canvas.get_tk_widget().destroy()
                self.canvas = FigureCanvasTkAgg(self.graph, master=right_frame)
                self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
                self.canvas.draw()
                self.loaded_graph = True
            except Exception as err:
                self.create_message_window(message=f"{str(type(err)).capitalize()}: {err}")

        def return_to_menu():
            """
            Funkcja zamyka aktualne okno i powraca do głównego menu programu.
            """
            root.destroy()
            self.start_program()

        # Przyciski
        ttk.Button(left_frame,
                   text="Załaduj Wykres",
                   command=generate_plot).grid(row=3,
                                               column=0,
                                               columnspan=1,
                                               pady=10)
        ttk.Button(left_frame,
                   text="Pobierz Załadowany Wykres",
                   command=save_as_pdf).grid(row=3,
                                             column=1,
                                             columnspan=1,
                                             pady=10)
        ttk.Button(left_frame,
                   text="Powrót",
                   command=return_to_menu).grid(row=3,
                                                column=2,
                                                columnspan=1,
                                                pady=10)

        # Konfiguracja proporcji dla ramek w okienku
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=2)
        root.grid_columnconfigure(1, weight=9)

        root.mainloop()