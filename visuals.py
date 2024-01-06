import seaborn as sns
import etl
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd


def create_scatter_plot(name_1 ='nazwa_1', name_2='nazwa_2', id_1='747060', id_2='747061'):
    df = etl.get_dataset(variables_dict={id_1: name_1, id_2:name_2})[['Location', name_1, name_2]]

    plt.figure(figsize=(12, 6))
    scatter_plot = sns.scatterplot(x=df[name_1], y=df[name_2], hue='Location', data=df, palette='viridis',
                                   legend='full', s=100)
    scatter_plot.legend(loc='upper left', bbox_to_anchor=(1, 1), borderaxespad=0.5)

    # Dodanie tytuł i oznaczenia osi
    plt.title('Wykres punktowy')
    plt.xlabel(name_1.capitalize(), wrap=True)
    plt.ylabel(name_2.capitalize(), wrap=True)
    plt.subplots_adjust(left=0.1, right=0.7, top=0.9, bottom=0.15)
    # plt.show()
    return plt.gcf()


def create_map(name_1='nazwa', id_1='747063'):
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

    return plt.gcf()


def create_bargraph(name_1='nazwa', id_1='747063'):
    df = etl.get_dataset(variables_dict={id_1: name_1})[['Location', name_1]]

    plt.bar(df['Location'], df[name_1], color='maroon',
            width=0.4)

    plt.title('Wykres kolumnowy')
    plt.xlabel("Województwo")
    plt.ylabel(name_1, wrap = True)
    plt.xticks(rotation=90)
    plt.subplots_adjust(left=0.2, right=0.95, top=0.95, bottom=0.4)
    return plt.gcf()

def create_piechart(name_1='nazwa', id_1='747063'):
    df = etl.get_dataset(variables_dict={id_1: name_1})[['Location', name_1]]
    colors = ("orange", "cyan", "brown", "grey", "indigo", "beige", "red", "blue", "green", "pink", "yellow", "purple",
              "turquoise", "violet", "coral", "olivedrab")
    plt.pie(df[name_1], labels=df['Location'], autopct='%1.1f%%', startangle=90, colors = colors)
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95, bottom=0.1)
    plt.title('Wykres kołowy')


    return plt.gcf()