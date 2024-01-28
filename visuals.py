import seaborn as sns
import etl
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import textwrap
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.preprocessing import StandardScaler


def wrap_labels(ax, width):
    """Funkcja służąca do zawijania etykiet na wykresie"""
    labels = []
    # Przetwarzanie etykiet osi X
    for label in ax.get_xticklabels():
        text = label.get_text()  # Pobieranie tekstu etykiety
        # Łamanie tekstu etykiety i dodanie do listy
        labels.append(textwrap.fill(text, width=width, break_long_words=True))
    # Ustawianie zmodyfikowanych etykiet na osi X z wyzerowanym kątem rotacji
    ax.set_xticklabels(labels, rotation=0)
    labels.clear()  # Czyszczenie listy etykiet

    # Przetwarzanie etykiet osi Y analogiczne do pierwszej częsci funckji
    for label in ax.get_yticklabels():
        text = label.get_text()
        labels.append(textwrap.fill(text, width=width, break_long_words=False))
    ax.set_yticklabels(labels, rotation=0)


def create_scatter_plot(name_1, name_2, id_1, id_2):
    """Funkcja zwracająca wykres punktowy zmiennych przekazanych jako parametr"""
    df = etl.get_dataset(variables_dict={id_1: name_1, id_2: name_2})[['Location', name_1, name_2]]

    plt.figure(figsize=(10, 5))

    scatter_plot = sns.scatterplot(x=df[name_1], y=df[name_2], hue='Location', data=df, palette='viridis',
                                   legend='full', s=100)
    scatter_plot.legend(loc='upper left', bbox_to_anchor=(1, 1), borderaxespad=0.5)

    # Dodanie tytuł i oznaczenia osi
    plt.title('Wykres punktowy')
    plt.xlabel(name_1.capitalize(), wrap=True)
    plt.ylabel(name_2.capitalize(), wrap=True)
    plt.subplots_adjust(left=0.1, right=0.7, top=0.9, bottom=0.15)
    return plt.gcf()


def create_map(name_1, id_1):
    """Funkcja zwracająca mapę polski z podzałem na województwa
    z naniesionymi wartościami  zmiennej przekazanej jako parametr"""
    df = etl.get_dataset(variables_dict={id_1: name_1})[['Location', name_1]]
    df['JPT_NAZWA_'] = df['Location'].astype(str).str.lower()
    df = df[['JPT_NAZWA_', name_1]]
    data = gpd.read_file(r'wojewodztwa/wojewodztwa.shp')
    merged_data = pd.merge(data, df, how='left', on='JPT_NAZWA_')

    fig, ax = plt.subplots(figsize=(10, 10))
    merged_data.plot(ax=ax, column=name_1, cmap='viridis', edgecolor='black', legend=True, legend_kwds={'shrink': 0.7})
    ax.set_xticks([])
    ax.set_yticks([])

    for x, y, name, value in zip(merged_data.geometry.centroid.x, merged_data.geometry.centroid.y,
                                 merged_data['JPT_NAZWA_'], merged_data[name_1]):
        label = f'\n{name}\n{value}'
        ax.text(x, y, label, fontsize=8, ha='center')
    plt.title(f'{name_1}'.capitalize(), wrap=True)
    # Zwrócenie obiektu wykresu
    return plt.gcf()


def create_heatmap(name_1, name_2, id_1, id_2):
    """Stworzenie wykresu korelacjii zmiennych wybranych jako parametr"""
    df = etl.get_dataset(variables_dict={id_1: name_1, id_2: name_2})[[name_1, name_2]].corr()
    plt.figure(figsize=(10, 5))
    heatmap = sns.heatmap(df, vmin=-1, vmax=1, linewidths=.5, annot=True, cmap="YlGnBu")
    # Dodanie tytułu i oznaczenia osi
    plt.subplots_adjust(left=0.3, right=0.9, top=0.9, bottom=0.3)
    heatmap.set(xlabel="", ylabel="", title='Heatmap')
    wrap_labels(heatmap, 25)
    # Zwrócenie obiektu wykresu
    return plt.gcf()


def create_dendrogram():
    """
    Tworzy dendrogram na podstawie podanych danych.
    """
    # Sprawdzenie, czy dane są w odpowiednim formacie
    df = etl.get_dataset().drop(columns=['Year'])

    # Wyodrębnienie danych miast i cech
    areas = list(df['Location'])
    features = df.drop(columns=['Location'], axis=1)

    # Normalizacja danych cech
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Obliczenie macierzy odległości i przeprowadzenie klastrowania
    linked = linkage(scaled_features, method='ward')

    # Rysowanie dendrogramu
    plt.figure(figsize=(10, 10))
    dendrogram(linked, orientation='right', labels=areas, distance_sort='ascending', leaf_rotation=15, truncate_mode = 'lastp')

    # Zaznaczenie linii poziomej reprezentującej podział na klastry
    plt.subplots_adjust(bottom=0.1, top=0.95, left=0.2, right=0.90)
    plt.title('Dendrogram Województw')
    plt.xlabel('Odległość w klastrze')
    plt.yticks(fontsize=9)
    return plt.gcf()


def create_bargraph(name_1, id_1):
    df = etl.get_dataset(variables_dict={id_1: name_1})[['Location', name_1]]

    plt.figure(figsize=(10, 6))  # Dodano utworzenie figury przed tworzeniem wykresu

    bar_plot = sns.barplot(data=df, x='Location', y=name_1,  ci=None)

    plt.title('Wykres kolumnowy')
    plt.xlabel("Województwo")
    plt.ylabel(name_1)
    plt.xticks(rotation=90)
    plt.subplots_adjust(left=0.2, right=0.95, top=0.95, bottom=0.4)

    return plt.gcf()


def create_piechart(name_1, id_1):
    df = etl.get_dataset(variables_dict={id_1: name_1})[['Location', name_1]]
    colors = sns.color_palette("pastel")  # Seaborn dostarcza palety kolorów, np. "pastel"

    plt.figure(figsize=(8, 8))  # Określ wielkość wykresu

    # Utwórz wykres kołowy przy użyciu Matplotlib i Seaborn
    plt.pie(df[name_1], labels=df['Location'], autopct='%1.1f%%', startangle=90, colors=colors)

    plt.title('Wykres kołowy')

    return plt.gcf()
