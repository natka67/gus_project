from matplotlib import pyplot as plt
import seaborn as sns
import etl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import geopandas as gpd

import os
def create_scatter_plot(name_1 = 'nazwa_1', name_2 = 'nazwa_2', id_1='747060',id_2='747061'):
    df = etl.get_dataset(variables_list=[id_1, id_2])[['Location',id_1, id_2]]

    plt.figure(figsize=(12, 6))
    scatter_plot = sns.scatterplot(x=df[id_1], y=df[id_2], hue='Location', data=df, palette='viridis', legend='full')
    scatter_plot.legend(loc='upper left', bbox_to_anchor=(1, 1), borderaxespad=0.5)

    # Dodaj tytuł i oznaczenia osi
    plt.title('Wykres punktowy')
    plt.xlabel(name_1.capitalize(), wrap=True)
    plt.ylabel(name_2.capitalize(), wrap=True)
    plt.subplots_adjust(left=0.1, right=0.7, top=0.9, bottom=0.15)
    #plt.show()
    return plt.gcf()


def create_map(name_1='nazwa', id_1='747063'):
    df = etl.get_dataset(variables_list=[id_1])[['Location',id_1]]
    df['JPT_NAZWA_'] = df['Location'].astype(str).str.lower()
    df = df[['JPT_NAZWA_', id_1]]
    data = gpd.read_file(r'wojewodztwa/wojewodztwa.shp')
    merged_data = pd.merge(data, df, how='left', on='JPT_NAZWA_')

    fig, ax = plt.subplots(figsize=(10, 10))
    merged_data.plot(ax=ax, column=id_1, cmap='viridis', edgecolor='black', legend=True)
    ax.set_xticks([])
    ax.set_yticks([])

    # Add labels on the districts
    for x, y, name, value in zip(merged_data.geometry.centroid.x, merged_data.geometry.centroid.y, merged_data['JPT_NAZWA_'], merged_data[id_1]):
        label = f'\n{name}\n{value}'
        ax.text(x, y, label, fontsize=8, ha='center')
    plt.title(f'{name_1}'.capitalize(), wrap=True)
    # plt.show()
    return plt.gcf()