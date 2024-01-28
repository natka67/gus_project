from tkinter import *
import gui
import etl
import pandas as pd
import xlsxwriter
import numpy as np

#data = etl.get_dataset()
data = pd.read_excel("gus.xlsx", usecols="B,D:S", index_col=0)
def create_ranking():
    #Tworzenie okna do metody TOPSIS
    root = Tk()
    root.title('Ranking województw - metoda TOPSIS')
    width = 1100
    height = 600
    root.geometry(f"{width}x{height}")
    center_x = int((root.winfo_screenwidth() - width) / 2)
    center_y = int((root.winfo_screenheight() - height) / 2)
    root.geometry(f"+{center_x}+{center_y}")

    #Lista z 3 rodzajami wpływu zmiennej na ranking
    options = ['stymulanta', 'destymulanta', 'brak wpływu']

    #Tworzenie listy z wpływem zmiennych na ranking
    choosingVariables = [StringVar() for _ in range(16)]

    #Określenie każdej zmiennej domyślnie jako stymulanta
    for i in choosingVariables:
        i.set(options[0])

    #Listy rozwijane
    listOfOptionMenu = []
    for var in choosingVariables:
        option_menu = OptionMenu(root, var, *options)
        listOfOptionMenu.append(option_menu)

    #Etykiety zmiennych
    labels = []
    for i in list(data.columns):
        l = Label(root, text=i)
        labels.append(l)

    #Wyświetlnie list rozwijanych z etykietami
    for index, (lab, mymenu) in enumerate(zip(labels, listOfOptionMenu)):
        lab.grid(row=index, column=0)
        mymenu.grid(row=index, column=1)


    impact = ['+' for i in range(16)]

    def download():
        #Lista zmiennych, które nie powinny mieć wpływu na ranking
        variables_to_drop = []
        for i in range(len(choosingVariables)):
            if choosingVariables[i].get() == 'destymulanta':
                impact[i] = '-'
            elif choosingVariables[i].get() == 'brak wpływu':
                variables_to_drop.append(i)

        #Usunięcie wpływu zmiennych, które nie powinny mieć wpływu na ranking
        for i in reversed(variables_to_drop):
            impact.pop(i)

        #Usunięcie zmiennych, które nie powinny mieć wpływu na ranking
        data.drop(data.columns[variables_to_drop], axis=1, inplace=True)

        #Wywołanie funkcji zwracającej ranking TOPSIS
        topsis_method(impact, data)
        #Wyświetlnie okna informującego o sukcesie
        gui.Gui().create_message_window()

    def return_to_menu():
        root.destroy()
        gui.Gui().start_program()

    button = Button(root, text="Pobierz ranking", command=download)
    button.grid(row = 17, column = 0)

    back = Button(root, text="Powrót", command=return_to_menu)
    back.grid(row = 18, column = 0)
    root.mainloop()

def topsis_method(impact, data):
    #Funkcja zwracjąca ranking, której argumentami jest zbiór danych i lista określająca wpływ każdej zmiennej
    listOfVariables = list(data.columns)

    data.iloc[:, 0:len(listOfVariables)] = data.iloc[:, 0:len(listOfVariables)].astype(float)
    for i in range(len(listOfVariables)):
        squartedSumOfxij = 0
        for j in range(len(data)):
            squartedSumOfxij = squartedSumOfxij + data.iloc[j, i] ** 2
        squartedSumOfxij = squartedSumOfxij**0.5

        for j in range(len(data)):
            data.iat[j, i] = data.iloc[j, i]/squartedSumOfxij
    idealBest = (data.max().values)
    idealWorst = (data.min().values)
    for i in range(len(listOfVariables)):
        if impact[i] == '-':
            idealBest[i], idealWorst[i] = idealWorst[i], idealBest[i]

    topsisScore = []
    distancePositive = []
    distanceNegative = []

    for i in range(len(data)):
        p, n = 0, 0
        for j in range(len(listOfVariables)):
            p = p + (idealBest[j] - data.iloc[i, j]) ** 2
            n = n + (idealWorst[j] - data.iloc[i, j]) ** 2
        p, n = p ** 0.5, n ** 0.5
        topsisScore.append(n / (p + n))
        distanceNegative.append(n)
        distancePositive.append(p)

    data['distance positive'] = distancePositive
    data['distance negative'] = distanceNegative
    data['Topsis Score'] = topsisScore

    data['Rank'] = (data['Topsis Score'].rank(method='max', ascending=False))
    data = data.astype({"Rank": int})
    ranking = data.iloc[:, -1]
    ranking.columns = ["Rank"]
    ranking = ranking.sort_values()
    ranking.to_excel("RankingTOPSIS.xlsx")



