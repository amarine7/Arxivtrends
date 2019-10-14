import pandas as pd
import feedparser

import datetime
import time

import methods



url_base = 'http://export.arxiv.org/api/query?search_query='
url_tail = '&max_results=10000'
#TODO choose how many MSCs and which one



class Scraper(object):
    """
    A class to specify the parameters of the scraping: a macrofield, the waiting
    time between subsequent calls to API, triggered by Error 503 (t), the timeout in
    seconds after which the scraping stops (default: 300s) and current date & time.

    Example:
    Returning all eprints from

    ```
        import arxivscraper.arxivscraper as ax
        scraper = ax.Scraper(macro_field='Harmonic Analysis', t=30, timeout=300)
        output = scraper.scrape()
    ```
    output is a df to which the graphical functions are to be applied. But scrape()
    also save a csv file with the same information as output, so we can get the
    same graphical results after the execution of the program ends.
    """

    def __init__(self, macro_field):

        try:
            self.url = url_base + url_query(macro_field) + url_tail
        except Exception:
            print("Error!")
            print("Research field not valid!")
        else:
            self.field = macro_field
            self.query_dict = feedparser.parse(self.url)

            if query_dict.status == 404:
                raise Exception("404 - Page Not Found")
                print("The query was unsuccessful, parsing cannot begin.")
            elif query_dict.status == 400:
                raise Exception("400 - Bad Request")
                print("The query was unsuccessful, parsing cannot begin.")
            elif query_dict.status == 200:
                print("The query was successful, parsing can begin now!")



    def scrape(self):

        years = []
        authors = []
        pages = []

        temporary_record = [0, [], 0]
        t0 = time.time()
        print("scraping started!"")
        for i in range(len(self.query_dict.entries)):

            if i%100 == 0:
                print("Total number of papers scraped: {:d}".format(i))
            record = self.query_dict.entries[i]

            temporary_record[0] = get_year(record.get('published'))
            if temporary_record[0] == None:
                continue

            temporary_record[1] = get_authors(record.get('authors'))
            if temporary_record[1] == None:
                continue

            temporary_record[2] = get_num_pages(record, i)
            if temporary_record[2] == None:
                continue

            years.append(temporary_record[0])
            authors.append(temporary_record[1])
            pages.append(temporary_record[2])

        # TODO print how many results, how many articles parsed, how many invalid

        t1 = time.time()

        records = pd.DataFrame({'years':years, 'authors':authors, 'pages': pages})
        query_details = get_details(macro_field)
        this.name_file = 'arXivQuery_' + query_details + '.csv'
        records.to_csv(this.name_file,  sep='\t', index = None, header=False)

        total_time = t1 - t0
        print('fetching is completed in ' + str(datetime.timedelta(seconds = x)) + ' hours.')
        print ('Total number of papers scraped: {:d}'.format(len(records)))

        return records



    def getUrl(self):
        return self.url

    def getField(self):
        return self.field

    def getNameFile(self):
        return this.name_file
