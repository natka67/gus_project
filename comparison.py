from tkinter import *
import pandas as pd
import etl
from gui import *

def start_functionality():
    root = Tk()
    root.title('Porównanie województw')
    height = 120
    width = 450
    root.geometry(f"{width}x{height}")
    center_x = int((root.winfo_screenwidth() - width) / 2)
    center_y = int((root.winfo_screenheight() - height) / 2)
    root.geometry(f"+{center_x}+{center_y}")

    voivodeships_poland = dict(pd.read_excel(r'system_data\voivodeships_poland.xlsx', dtype={'id': str})[['id', 'name']].values)

    voivodeship1 = StringVar()
    voivodeship2 = StringVar()
    voivodeship1.set("WIELKOPOLSKIE")
    voivodeship2.set("POMORSKIE")

    drop1 = OptionMenu(root, voivodeship1, *voivodeships_poland.values())
    drop2 = OptionMenu(root, voivodeship2, *voivodeships_poland.values())
    drop1.pack()
    drop2.pack()

    def button_clicked():
        selected1 = voivodeship1.get()
        selected2 = voivodeship2.get()
        voivodeships = [key for key, value in voivodeships_poland.items() if value in [selected1, selected2]]
        download_comparison(voivodeships)

    def return_to_menu():
        root.destroy()
        Gui().start_program()

    button = Button(root, text="Pobierz Porównanie", command=button_clicked)
    button.pack()

    back = Button(root, text="Powrót", command=return_to_menu)
    back.pack()
    root.mainloop()

def download_comparison(voivodeships):
    df = etl.get_dataset(voivodeships_poland=voivodeships).T
    df.columns = df.iloc[0]
    df = df.iloc[3:]
    df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
    df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors='coerce')
    df['Comparison'] = df.iloc[:, 0] - df.iloc[:, 1]
    df.to_excel(f'porównanie_{'_'.join(df.columns)}.xlsx')
    Gui().create_message_window()

