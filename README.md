# arXivTrends

An ArXiV scraper to retrieve records from given research areas in mathematics and detect some trends in hyper-specialization and growth rate increase of scientific production in those fields.

## Install
Use the package manager [pip](https://pip.pypa.io/en/stable/) or ```pip3``` for python3):

```bash
$ pip install arxivtrends
```

or download the source and use ```setup.py```:

```bash
$ python setup.py install
```

To update the module using ```pip```:

```bash
$ pip install arxivtrends --upgrade
```

## Examples
Let's import ```arxivtrends``` and create a scraper to fetch all preprints in Fourier analysis (for other fields see below):

```python
import arxivtrends
scraper = arxivtrends.Scraper(macro_field='Harmonic analysis')
```

The instantiation of the class ```Scraper``` with the parameter ```macro_field``` set to 'Harmonic analysis' returns a dictionary-like object containing all the information (authors, title, date of publication, etc.) about the preprints in the arXiv whose [Mathematics Subject Classification (MSC)](https://cran.r-project.org/web/classifications/MSC-2010.html) falls under the category Harmonic analysis on Euclidean spaces.

Once ```scraper``` is built, we can start parsing it to extract the information we want for each preprint: year of publication, list of authors and number of pages.

```python
output_df = scraper.scrape()
```

While ```scrape()``` is running, it prints its status:

```python
fetched N papers
...
```

Finally the extracted information is saved both into the pandas DataFrame ```output_df``` and into a ```.csv``` file. The latter option may be useful in case of overnight running and kernel shutdown, as the parsing process may last up to a few hours (see (...)).

Once the parsing is complete, we can call the data visualization methods (see the script ```graphics.py```) and see what the data can tell us. For example, the method ```plot_N_authors_papers()``` shows the number of uploaded arXiv preprints with at least ```N``` authors year by year:

```python
plot_N_authors_papers(output_df, 3)
INSER PICTURE HERE !!!
```

## Research Areas
```Harmonic analysis on Euclidean spaces``` (MSC codes: 42A05 - 42C40), ```Abstract harmonic analysis``` (MSC codes: 43A05 - 43A90), ```Partial differential equations of elliptic type``` (MSC codes: 35J05 - 35J85), ```Partial differential equations of fluid mechanics``` (MSC codes: 76A02 - 76S05).


## License
[MIT](https://choosealicense.com/licenses/mit/)
