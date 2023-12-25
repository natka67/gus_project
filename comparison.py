from tkinter import *
import gui
import etl
import pandas as pd
import xlsxwriter



def compare():
    root = Tk()
    root.title('Porównanie województw')
    width = 450
    height = 120
    root.geometry(f"{width}x{height}")
    center_x = int((root.winfo_screenwidth() - width) / 2)
    center_y = int((root.winfo_screenheight() - height) / 2)
    root.geometry(f"+{center_x}+{center_y}")

    voivodeships_poland = dict(pd.read_excel('voivodeships_poland.xlsx', dtype={'id': str})[['id', 'name']].values)

    voivodeship1 = StringVar()
    voivodeship2 = StringVar()
    voivodeship1.set("WIELKOPOLSKIE")
    voivodeship2.set("POMORSKIE")

    drop1 = OptionMenu(root, voivodeship1, *voivodeships_poland.values())
    drop2 = OptionMenu(root, voivodeship2, *voivodeships_poland.values())
    drop1.pack()
    drop2.pack()

    def download():
        selected1 = voivodeship1.get()
        selected2 = voivodeship2.get()
        voivodeships = [key for key, value in voivodeships_poland.items() if value in [selected1, selected2]]
        download_comparison(voivodeships)

    def return_to_menu():
        root.destroy()
        gui.Gui().start_program()

    button = Button(root, text="Pobierz Porównanie", command=download)
    button.pack()

    back = Button(root, text="Powrót", command=return_to_menu)
    back.pack()
    root.mainloop()


def download_comparison(voivodeships):
    try:
        df = etl.get_dataset(voivodeships_poland=voivodeships).T
        df.columns = df.iloc[0]
        df = df.iloc[3:]
        df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
        df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors='coerce')
        df['Comparison'] = df.iloc[:, 0] - df.iloc[:, 1]

        with pd.ExcelWriter(f'porównanie_{'_'.join(df.columns)}.xlsx', engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=True, header=True)

            # Get the xlsxwriter workbook and worksheet objects.
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']

            # Get the number of rows and columns in the dataframe.
            num_rows, num_cols = df.shape

            # Create a Pandas Excel writer using XlsxWriter as the engine.
            red_format = workbook.add_format({'font_color': 'red'})
            green_format = workbook.add_format({'font_color': 'green'})
            black_format = workbook.add_format({'font_color': 'black'})

            # Apply the conditional formatting based on the specified condition.
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

        #df.to_excel(f'porównanie_{'_'.join(df.columns)}.xlsx')
    except Exception as err:
        gui.Gui().create_message_window(message=f"{str(type(err)).capitalize()}: {err}")
