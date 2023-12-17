# Import module
from tkinter import *
import pandas as pd
def create_window():
    # Create object
    root = Tk()

    # Adjust size
    height = 120
    width = 450
    root.geometry(f"{width}x{height}")
    center_x = int((root.winfo_screenwidth() - width) / 2)
    center_y = int((root.winfo_screenheight() - height) / 2)
    root.geometry(f"+{center_x}+{center_y}")
    voivodeships_poland = dict(pd.read_excel('voivodeships_poland.xlsx', dtype={'id': str})[['id', 'name']].values)


    # datatype of menu text
    voivodeship1 = StringVar()
    voivodeship2 = StringVar()

    # initial menu text
    voivodeship1.set("WIELKOPOLSKIE")
    voivodeship2.set("POMORSKIE")

    # Create Dropdown menu
    drop1 = OptionMenu(root, voivodeship1, *voivodeships_poland.values())
    drop2 = OptionMenu(root, voivodeship2, *voivodeships_poland.values())
    drop1.pack()
    drop2.pack()


    # Execute tkinter
    root.mainloop()

def download_comparison():
    create_window()
    pass