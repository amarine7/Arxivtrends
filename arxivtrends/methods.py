import re
import urllib
from PyPDF2 import PdfFileReader
from PyPDF2.utils import PdfReadError
from io import BytesIO
import datetime
import numpy as np



macro_fields = {
    'Partial differential equations of elliptic type':['35J05', '35J10', '35J15', '35J20', '35J25', '35J30', '35J35', '35J40', '35J45', '35J50', '35J55', '35J60', '35J65', '35J67', '35J70', '35J85'],
    'Harmonic analysis on Euclidean spaces':['42A05', '42A10', '42A15', '42A16', '42A20', '42A24', '42A32', '42A38', '42A45', '42A50', '42A55', '42A61', '42A63', '42A65', '42A70', '42A75', '42A82', '42A85', '42B05', '42B08', '42B10', '42B15', '42B20', '42B25', '42B30', '42B35', '42C10', '42C15', '42C20', '42C25', '42C30', '42C40'],
    'Abstract harmonic analysis':['43A05', '43A07', '43A10', '43A15', '43A17', '43A20', '43A22', '43A25', '43A30', '43A32', '43A35', '43A40', '43A45', '43A46', '43A50', '43A55', '43A60', '43A62', '43A65', '43A70', '43A75', '43A77', '43A80', '43A85', '43A90'],
    'Partial differential equations of fluid mechanics': ['76A02','76A05','76A10','76A15','76A20','76A25','76A99','76B03','76B07','76B10','76B15','76B20','76B25','76B45','76B47','76B55','76B60','76B65','76B70','76D03','76D05','76D06','76D07','76D08','76D09','76D10','76D17','76D25','76D27','76D33','76D45','76D50','76D55','76E05','76E06','76E07','76E09','76E15','76E17','76E19','76E20','76E25','76E30','76E99','76Fxx','76F02','76F05','76F06','76F10','76F20','76F25','76F30','76F35','76F40','76F45','76F50','76F55','76F60','76F65','76F70','76F99','76G25]','76H05','76J20','76K05','76L05','76M10','76M12','76M15','76M20','76M22','76M23','76M25','76M27','76M28','76M30','76M35','76M40','76M45','76M50','76M55','76M60','76N10','76N15','76N17','76N20','76N25','76N99','76P05','76Q05','76Rxx','76R05','76R10','76R50', '76S05']
}

def url_query(macro_field):
    if macro_field in macro_fields.keys():
        list = macro_fields.get(macro_field)
        for subfield in list[1:]:
            list[0] = list[0] + '+OR+all:' + subfield
        return 'all:' + list[0]
    else:
        raise



def get_authors(authors):
    if len(authors) == 0:
        return None
    else:
        list_authors = [];
        for researcher in authors:
            list_authors.append(researcher.get('name'))
        return list_authors



def get_num_pages(record, i):
    if record.get('arxiv_comment') == None:
        if record.get('arxiv_journal_ref') == None:
            return pages_from_url(record, i)
        else:
            return pages_from_journal(record)
    else:
        pages = find_match(0, record.get('arxiv_comment'))
        if pages == None:
            pages = pages_from_journal(record)
            if pages == None:
                pages = find_match(1, record.get('arxiv_comment'))
                if pages == None:
                    pages = find_match(2, record.get('arxiv_comment'))
                    if pages == None:
                        pages = pages_from_url(record, i)
    return pages




def pages_from_journal(record):
    if record.get('arxiv_journal_ref') == None:
        return None
    else:
        pattern = re.compile(r'(.\d\d-\d\d.|\d\d-\d\d|.\d\d-\d\d\d|\d\d\d\d-\d\d\d\d)')
        matches = pattern.findall(record.get('arxiv_journal_ref'))
        if len(matches) == 1 and len(re.findall(r'\d+', matches[0])) == 2:
            pages = int(re.findall(r'\d+', matches[0])[1]) - int(re.findall(r'\d+', matches[0])[0])
        else:
            pages = None
    return pages




# explain that the last two options are way less likely to occur, that's
# why we did not use or for the options page, pp, pgs at the same level
def find_match(i, text):
    if i == 0:
        pattern = re.compile(r'(...page|....page)')
    if i == 1:
        pattern = re.compile(r'(...pp|....pp)')
    if i == 2:
        pattern = re.compile(r'(...pgs|....pgs)')
    matches = pattern.findall(text)
    if len(matches) > 0:
        for match in matches:
            pass
        if len(re.findall(r'\d+', match)) > 0:
            return int(re.findall(r'\d+', match)[-1])
        else:
            #print("no nummber before the alphabetical match")
            return None
    else:
        #print("no alphabetical match in the text")
        return None




def pdf_url(url_text):
    return re.sub("abs", "pdf", url_text)




def pages_from_url(record, i):
    url = pdf_url(record.get('id'))
    try:
        time.sleep(np.max([i%7, 3]))
        link = urllib.request.urlopen(url)
        content=link.read()
        memoryFile = BytesIO(content)
        pdfFile = PdfFileReader(memoryFile)
        return pdfFile.getNumPages()
    except PdfReadError:
        return None
    except urllib.error.HTTPError:
        return None



def get_year(record):
    num = record[:4]
    if len(num) == 4 and num.isdigit():
        return int(num)
    else:
        return None



def get_details(macro_field):
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    return macro_field + '_' + str(now)
