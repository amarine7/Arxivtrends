"""
the methods of graphics.py are to be used once the parsing loop triggered by the
parse() method is complete, as they concern the (now clean) data loading from
file and graphical visualization.
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import collections

# not necessary:
#df['years'] = df['years'].astype('int')
#df['pages'] = df['pages'].astype('int')


"""
the scrape method saves the lists of authors of the parsed preprints as strings
in the .csv file once the parsing loop is complete. When we load the data from
the file, we need to turn these strings back into lists of authors. The
string_to_list method splits these strings and removes the bracket characters.
"""
def string_to_list(string):
    return string.strip('[').strip(']').split(',')




"""
method to retrieve the research field from the name of the file .csv containing
the clean data relative to that field. The string representing the research field
is returned as a list of length 1 because we want to use it to give a name to the
index column of the DataFrame into which we load the data (see load_data()).
"""
def get_field_from_file(name_file):
    lst = []
    text = name_file.split('__')[1]
    lst.append(re.sub("_", " ", text))
    return lst





"""
method to load the clean data (created by the scrape() method) from a .csv file
into a DataFrame. We assign the name of the research field to the index column,
turn the type of the 'authors' column from string to list and return the final
DataFrame.
"""
def load_data(name_file):
    df = pd.read_csv(name_file, sep='\t', names=['years', 'authors', 'pages'])
    df.index.names = get_field_from_file(name_file)
    list_authors = [string_to_list(string) for string in df['authors']]
    df = df.drop('authors', axis=1)
    df['authors'] = list_authors
    df['#authors'] = [len(list) for list in df['authors']]
    return df






"""
method to show the bar graph of submitted arXiv preprints in a chosen research
field with at least N authors on a yearly basis.
"""
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
    plt.title('Preprints in ' + df.index.names[0] + ' by ' + str(N) ' or more authors')
    #plt.show()





"""
method to show the plot of the mean number of authors (graph above) and mean
number of pages of all submitted arXiv preprints in a chosen research field on a
yearly basis.
"""
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
    ax1.set_title('Average Number of Authors of ArXiv Preprints by Year')
    ax2.set_title('Average Number of Pages of ArXiv Preprints by Year')
    ax1.grid(True)
    ax2.grid(True)
    fig.tight_layout()
    #plt.show()






def average_productivity():
    pass

    #Select the year from which to count, then for each author who started publishing
    #in that year  consider the number of papers published every year. Then, for
    #each year, calculate the average of that value

    #Use update to append set with an iterable: a.update([3,4])







#Per aggiungere le spiegazioni alle celle di codice jn, seleziona altre celle
#come markdown: #Cell -> Cell Type

#! + command in jn is like a command given from cmd line


#in the ipynb file usare %matplotlib inline per far vedere le immagini, ma dire che è meglio
#usare %matplotlib qt. For other fields, just save the pictures you get this last way




#for quartiles:
    #df2 = df.groupby('years')['#authors'].describe()
    #df3 = df2[['mean', '25%', '50%', '75%']]
