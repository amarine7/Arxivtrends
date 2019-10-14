import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import collections

# not necessary:
#df['years'] = df['years'].astype('int')
#df['pages'] = df['pages'].astype('int')



def string_to_list(string):
    return string.strip('[').strip(']').split(',')



def load_data(name_file):
    df = pd.read_csv(name_file, sep='\t', names=['years', 'authors', 'pages'])
    list_authors = [string_to_list(string) for string in df['authors']]
    df = df.drop('authors', axis=1)
    df['authors'] = list_authors
    df['#authors'] = [len(list) for list in df['authors']]
    return df



def plot_N_authors_papers(df, N):
    df2 = df[df['#authors']>N]
    histogram = collections.Counter(df2['years'])

    plt.rcParams['figure.figsize'] = [20, 8]
    bucket_size = 0.8
    plt.bar(histogram.keys(), histogram.values(), bucket_size, align='center', edgecolor='black')
    plt.xlabel('years')
    plt.ylabel('papers')
    plt.grid(True)
    list_indexes = np.arange(df2['years'].min(), 2020, 1)
    list_labels = [str(year) for year in list_indexes]
    plt.xticks(ticks=list_indexes, labels=list_labels, rotation=50)
    #plt.show()



def mean_authors_vs_pages(df):
    labels = np.arange(2002, 2020, 2)
    df2 = df[df['years'] >= 2002]
    df3 = df2.groupby('years')['#authors', 'pages'].mean()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 7), sharex=True)
    ax1.plot(df3.index, df4['#authors'], marker='o', linewidth=1)
    ax2.plot(df3.index, df4['pages'], marker='o', linewidth=1)
    ax2.set_xlabel('years')
    ax1.set_ylabel('authors')
    ax2.set_ylabel('pages')
    ax2.set_xticks(labels)
    ax1.set_title('Average Number of Authors of Published Papers by Year')
    ax2.set_title('Average Number of Pages by Year')
    ax1.grid(True)
    ax2.grid(True)
    fig.tight_layout()
    #plt.show()






def average productivity():
    pass

    #Select the year from which to count, then for each author who started publishing
    #in that year  consider the number of papers published every year. Then, for
    #each year, calculate the average of that value

    #Use update to append set with an iterable: a.update([3,4])





#aggiungere un file .mb per spiegazioni di base e istallazione, dopodiché fare
#un file ipynb con un esempio di uso completo del pacchetto + spiegazioni di quello che uno
#vede e interpretazione dei risultati. Resta aperta l'opzione di come dare
#delle spiegazioni dettagliate del codice (nei files o in un altro md, etc.). Per aggiungere
#le spiegazioni alle celle di codice jn, seleziona altre celle come markdown:
#Cell -> Cell Type

#! + command in jn is like a command given from cmd line


#in the ipynb file usare %matplotlib inline per far vedere le immagini, ma dire che è meglio
#usare %matplotlib qt. For other fields, just save the pictures you get this last way















#for quartiles:
    #df2 = df.groupby('years')['#authors'].describe()
    #df3 = df2[['mean', '25%', '50%', '75%']]
