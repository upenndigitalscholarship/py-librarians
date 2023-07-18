#Script to scrape subject headings for journals

#Citation: Shelly R. McDavid, Eric McDavid, and Neil E. Das. "Leveraging a Custom Python Script to Scrape Subjecy Headings for Journals". Code4Lib Journal, issue 52, 2021. https://journal.code4lib.org/articles/16080.
#Script also housed at https://github.com/smcdavi/subjectscraper.py/blob/master/subjectscraper.py
#Detailed rationale and walkthrough available at the above source!


from urllib.request import urlopen 
from bs4 import BeautifulSoup 
from tqdm import tqdm 
import re, argparse, sys, csv, time 
   
catalogs = { 
    #'catalog name' : { 
    #   'base_url' : beginning part of URL from 'http://' to before first '/', 
    #   'search_url' : URL for online catalog search without base URL including '/'; 
    #                   make sure that '{0}' is in the proper place for the query of ISSN, 
    #   'search_title' : CSS selector for parent element of anchor 
    #                    containing the journal title on search results in HTML, 
    #   'bib_record' : CSS selector for record metadata on catalog item's HTML page, 
    #   'bib_title' : CSS selector for parent element of anchor containing the journal title, 
    #   'bib_subjects' : HTML selector for specific table element where text begins with 
    #                     "Topics", "Subject" in catalog item's HTML page in context of bib_record 
    'worldcat' : { 
        'base_url' : "https://www.worldcat.org", 
        'search_url' : "/search?qt=worldcat_org_all&q={0}", 
        'search_title' : ".result.details .name", 
        'bib_record' : "div#bibdata", 
        'bib_title' : "div#bibdata h1.title", 
        'bib_subjects' : "th"
    }, 
    'carli_i-share' :  { 
        'base_url' : "https://vufind.carli.illinois.edu", 
        'search_url' : "/all/vf-sie/Search/Home?lookfor={0}&type=isn&start_over=0&submit=Find&search=new", 
        'search_title' : ".result .resultitem", 
        'bib_record' : ".record table.citation", 
        'bib_title' : ".record h1", 
        'bib_subjects' : "th"
    }, 
    'mobius' : { 
        'base_url' : 'https://searchmobius.org', 
        'search_url' : "/iii/encore/search/C__S{0}%20__Orightresult__U?lang=eng&suite=cobalt", 
        'search_title' : ".dpBibTitle .title", 
        'bib_record' : "table#bibInfoDetails", 
        'bib_title' : "div#bibTitle", 
        'bib_subjects' : "td"
    } 
} 
   
# Obtain the right parameters for specific catalog systems 
# Input: catalog name: 'worldcat', 'carli i-share', 'mobius' 
# Output: dictionary of catalog parameters 
def get_catalog_params(catalog_key): 
    try: 
        return catalogs[catalog_key] 
    except: 
        print('Error - unknown catalog %s' % catalog_key) 
   
# Search catalog for item by ISSN 
# Input: ISSN, catalog parameters 
# Output: full URL for catalog item 
def search_catalog (issn, p = catalogs['carli_i-share']): 
    title_url = None
    # catalog url for searching by issn 
    url = p['base_url'] + p['search_url'].format(issn) 
    u = urlopen (url) 
    try: 
        html = u.read().decode('utf-8') 
    finally: 
        u.close() 
    try: 
        soup = BeautifulSoup (html, features="html.parser") 
        title = soup.select(p['search_title'])[0] 
        title_url = title.find("a")['href'] 
    except: 
        print('Error - unable to search catalog by ISSN') 
        return title_url 
    return p['base_url'] + title_url 
   
# Scrape catalog item URL for metadata 
# Input: full URL, catalog parameters 
# Output: dictionary of catalog item metadata, 
#   including title and subjects 
def scrape_catalog_item(url, p = catalogs['carli_i-share']): 
    result = {'title':None, 'subjects':None} 
    u = urlopen (url) 
    try: 
        html = u.read().decode('utf-8') 
    finally: 
        u.close() 
    try: 
        soup = BeautifulSoup (html, features="html.parser") 
        # title 
        try: 
            title = soup.select_one(p['bib_title']).contents[0].strip() 
            # save title to result dictionary 
            result["title"] = title 
        except: 
            print('Error - unable to scrape title from url') 
        # subjects 
        try: 
            record = soup.select_one(p['bib_record']) 
            subject = record.find_all(p['bib_subjects'], string=re.compile("(Subjects*|Topics*)"))[0] 
            subject_header_row = subject.parent 
            subject_anchors = subject_header_row.find_all("a") 
            subjects = [] 
            for anchor in subject_anchors: 
                subjects.append(anchor.string.strip()) 
            # save subjects to result dictionary 
            result["subjects"] = subjects 
        except: 
            print('Error - unable to scrape subjects from url') 
    except: 
        print('Error - unable to scrape url') 
    return result 
   
# Search for catalog item and process metadata from item's HTML page 
# Input: ISSN, catalog paramters 
# Output: dictionary of values: issn, catalog url, title, subjects 
def get_issn_data(issn, p = catalogs['carli_i-share']): 
    results = {'issn':issn, 'url':None, 'title':None, 'subjects':None} 
    time.sleep(time_delay) 
    url = search_catalog(issn, params) 
    results['url'] = url 
    if url: # only parse metadata for valid URL 
        time.sleep(time_delay) 
        item_data = scrape_catalog_item(url, params) 
        results['title'] = item_data['title'] 
        if item_data['subjects'] is not None: 
            results['subjects'] = ','.join(item_data['subjects']).replace(', -', ' - ') 
    return results 
   
# main loop to parse all journals 
time_delay = 0.5 # time delay in seconds to prevent Denial of Service (DoS) 
try: 
    # setup arguments for command line 
    args = sys.argv[1:] 
    parser = argparse.ArgumentParser(description='Scrape out metadata from online catalogs for an ISSN') 
    parser.add_argument('catalog', type=str, choices=('worldcat', 'carli_i-share', 'mobius'), help='Catalog name') 
    parser.add_argument('-b', '--batch', nargs=1, metavar=('Input CSV'), help='Run in batch mode - processing multiple ISSNs') 
    parser.add_argument('-s', '--single', nargs=1, metavar=('ISSN'), help='Run for single ISSN') 
    args = parser.parse_args() 
   
    params = get_catalog_params(args.catalog) # catalog parameters 
    # single ISSN 
    if args.single is not None:  
        issn = args.single[0] 
        r = get_issn_data(issn, params) 
        print('ISSN: {0}\r\nURL: {1}\r\nTitle: {2}\r\nSubjects: {3}'.format(r['issn'], r['url'], r['title'], r['subjects'])) 
    # multiple ISSNs 
    elif args.batch is not None:  
        input_filename = args.batch[0] 
        output_filename = 'batch_output_{0}.csv'.format(args.catalog) # put name of catalog at end of output file 
        with open(input_filename, mode='r') as csv_input, open(output_filename, mode='w', newline='', encoding='utf-8') as csv_output: 
            read_in = csv.reader(csv_input, delimiter=',') 
            write_out = csv.writer(csv_output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL) 
            write_out.writerow(['ISSN', 'URL', 'Title', 'Subjects']) # write out headers to output file 
            total_rows = sum(1 for row in read_in) # read all rows to get total 
            csv_input.seek(0) # move back to beginning of file 
            read_in = csv.reader(csv_input, delimiter=',') # reload csv reader object 
            for row in tqdm(read_in, total=total_rows): # tqdm is progress bar 
                # each row is an ISSN 
                issn = row[0] 
                r = get_issn_data(issn, params) 
                write_out.writerow([r['issn'], r['url'], r['title'], r['subjects']]) 
except Exception as e: 
    print(e) 