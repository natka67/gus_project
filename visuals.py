from matplotlib import pyplot as plt
from matplotlib import text as mtext
import seaborn as sns
import etl
def create_scatter_plot(name_1 = 'nazwa_1', name_2 = 'nazwa_2', id_1='747060',id_2='747061'):
    df = etl.get_dataset(variables_list=[id_1, id_2])[['Location',id_1, id_2]]

    plt.figure(figsize=(12, 6))
    scatter_plot = sns.scatterplot(x=df[id_1], y=df[id_2], hue='Location', data=df, palette='viridis', legend='full')
    scatter_plot.legend(loc='upper left', bbox_to_anchor=(1, 1), borderaxespad=0.5)

    # Dodaj tytuł i oznaczenia osi
    plt.title('Wykres punktowy')
    plt.xlabel(name_1, wrap=True)
    plt.ylabel(name_2, wrap=True)
    plt.subplots_adjust(left=0.1, right=0.7, top=0.9, bottom=0.15)
    #plt.show()
    return plt.gcf()


def create_map(col_name):
    print('Mapa Huncwotów, potrzebne hasło')
    'Mapa wyswietli się po wpisaniu hasła z Harry pottera'


create_scatter_plot()