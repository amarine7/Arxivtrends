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
A not None test is unnecessary: all the strings loaded from the file that
scrape() creates have the form '[...]'.
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
    plt.ylabel('preprints')
    plt.grid(True)
    list_indexes = np.arange(df2['years'].min(), df2['years'].max(), 1)
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






def find_pool_authors(df):
    authors_pool = set()
    for authors in df['authors']:
        authors_pool.update(authors)
    return authors_pool



#change the iteration over df, see
# https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
# [x['field'] for x in df] is wrong it causes the error string indices must be integers
def get_productivity_database(df):
    authors_pool = find_pool_authors(df)
    preprints = 0
    authors_df = pd.DataFrame([], columns = ['author' , 'year', '#preprints'])
    for author in authors_pool:
        for year in range(df['years'].min(), df['years'].max()):
            preprints = 0
            for record in df:
                if author in record['authors'] and year == record['years']:
                    preprints+=
            authors_df = authors_df.append({'author':author , 'year':year, '#preprints':preprints}, ignore_index=True)
    return authors_df





def average_productivity(authors_df, year):
    filtered_df = authors_df.drop(authors_df[authors_df['#preprints'] == 0].index)
    filtered_df = filtered_df.groupby('author').filter(lambda x:x['year'].min() == year)
    filtered_df = filtered_df.groupby('year')['#preprints'].mean()

    plt.rcParams['figure.figsize'] = [20, 8]
    plt.plot(filtered_df['year'], filtered_df['#preprints'], marker='o', linewidth=1)
    plt.xlabel('years')
    plt.ylabel('preprints')
    plt.grid(True)
    list_indexes = np.arange(year, filtered_df['years'].max(), 1)
    list_labels = [str(year) for year in filtered_df['year']]
    plt.xticks(ticks=list_indexes, labels=list_labels, rotation=50)
    plt.title('Average research production from authors whose first preprint was submitted in ' + str(year) + '.')
    #plt.show()
