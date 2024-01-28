from tkinter import *
import gui
import etl
import pandas as pd


def compare():
    """Funkcja tworząca okno pozwalające na stworzenie porównania województw"""

    # Ustawienie okna głównego
    root = Tk()
    root.title('Porównanie województw')
    width = 450
    height = 120
    root.geometry(f"{width}x{height}")
    center_x = int((root.winfo_screenwidth() - width) / 2)
    center_y = int((root.winfo_screenheight() - height) / 2)
    root.geometry(f"+{center_x}+{center_y}")

    # Wczytanie danych o województwach
    voivodeships_poland = dict(pd.read_excel('voivodeships_poland.xlsx', dtype={'id': str})[['id', 'name']].values)

    # Ustawienie wartosci początkowych dla rozwijanych list
    voivodeship1 = StringVar()
    voivodeship2 = StringVar()
    voivodeship1.set("WIELKOPOLSKIE")
    voivodeship2.set("POMORSKIE")

    # Tworzenie pól z listami rozwijanymi
    drop1 = OptionMenu(root, voivodeship1, *voivodeships_poland.values())
    drop2 = OptionMenu(root, voivodeship2, *voivodeships_poland.values())
    drop1.pack()
    drop2.pack()

    def download():
        """Funkcja pobierająca porównanie"""
        selected1 = voivodeship1.get()
        selected2 = voivodeship2.get()
        voivodeships = [key for key, value in voivodeships_poland.items() if value in [selected1, selected2]]
        download_comparison(voivodeships)

    def return_to_menu():
        """Funkcja przenosząca użytkownika do okna startowego"""
        root.destroy()
        gui.Gui().start_program()

    #Dodanie przycisków pobierającego porównanie i przenoszącego użytkownika do okna startowego
    button = Button(root, text="Pobierz Porównanie", command=download)
    button.pack()
    back = Button(root, text="Powrót", command=return_to_menu)
    back.pack()

    root.mainloop()


def download_comparison(voivodeships):
    """Funkcja do stworzenia i zapisania porównania województw"""
    try:
        #Pobranie danych
        df = etl.get_dataset(voivodeships_poland=voivodeships).T
        df.columns = df.iloc[0]
        df = df.iloc[3:]
        df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
        df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors='coerce')
        df['Comparison'] = df.iloc[:, 0] - df.iloc[:, 1]

        # Zapis danych do pliku Excel z zaaplikowanym formatowaniem warunkowym
        with pd.ExcelWriter(f"porównanie_{'_'.join(df.columns)}.xlsx", engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=True, header=True)

            workbook = writer.book
            worksheet = writer.sheets['Sheet1']

            num_rows, num_cols = df.shape

            # Zdefiniowanie kolorów aplikowanych dla wartości dodatnich, ujemnych oraz zera.
            red_format = workbook.add_format({'font_color': 'red'})
            green_format = workbook.add_format({'font_color': 'green'})
            black_format = workbook.add_format({'font_color': 'black'})

            # Zaaplikowanie kolorów w pliku Excela na wartościach w ostatniej kolumnie
            for row in range(1, num_rows + 1):
                worksheet.conditional_format(row, num_cols, row, num_cols,
                                             {'type': 'cell',
                                              'criteria': '<',
                                              'value': 0,
                                              'format': red_format})

                worksheet.conditional_format(row, num_cols, row, num_cols,
                                             {'type': 'cell',
                                              'criteria': '=',
                                              'value': 0,
                                              'format': black_format})

                worksheet.conditional_format(row, num_cols, row, num_cols,
                                             {'type': 'cell',
                                              'criteria': '>',
                                              'value': 0,
                                              'format': green_format})

    except Exception as err:
        """ Wyświetlanie okna z komunikatem o błędzie """
        gui.Gui().create_message_window(message=f"{str(type(err)).capitalize()}: {err}")
