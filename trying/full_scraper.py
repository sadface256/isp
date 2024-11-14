import csv
from crossword_scraper import scrape
from xwordinfo import parse_crossword
import pandas as pd

def build_urls():
    #first crossword was on 2/15/1942
    #crosswords became daily on 9/10/1950
    #last ps puzzle is 11/20/1993
    #crosswords up to today 10/17/2024
    #s1 = now.strftime("%m/%d/%Y)
    ps_sunday_dates = pd.date_range(start='2/15/1942', end='9/10/1950', freq='W').strftime("%m/%d/%Y").tolist()
    ps_later_dates = pd.date_range(start='9/11/1950', end='11/20/1993', freq='D').strftime("%m/%d/%Y").tolist()
    crossword_dates = pd.date_range(start='11/21/1993', end='10/17/2024', freq='D').strftime("%m/%d/%Y").tolist()
    ps_sunday_urls = ["https://www.xwordinfo.com/PS?date=" + date for date in ps_sunday_dates]
    ps_later_urls = ["https://www.xwordinfo.com/PS?date=" + date for date in ps_later_dates]
    crossword_urls = ["https://www.xwordinfo.com/Crossword?date=" + date for date in crossword_dates]
    ps_sunday_urls.append(ps_later_urls)
    ps_sunday_urls.append(crossword_urls)
    ps_later_urls.extend(crossword_urls)
    return ps_later_urls#ps_sunday_urls

# def scraper():
#     with open('test_csv.csv', 'w', newline='') as f:
#         list_urls = build_urls()
#         writer = csv.writer(f)
#         writer.writerow(['CLUE', 'ANSWER', 'AUTHOR', 'EDITOR', 'LINK', 'DATE'])
#         for url in list_urls:
#             scrape(writer, url)

def scraper():
    list_urls = build_urls()
    for url in list_urls:
        date = url.split("=")[1].replace("/", "_")
        with open('crossword_data/' + date + '.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['CLUE', 'ANSWER', 'AUTHOR', 'EDITOR', 'LINK', 'DATE'])
            scrape(writer, url)
            print('Done with ' + date + "!")

def json_scraper():
    list_urls = build_urls()
    for url in list_urls:
        date = url.split("=")[1].replace("/", "_")
        with open('json_crossword_data/' + date + '.json', 'w', newline='') as f:
            #writer = csv.writer(f)
            #writer.writerow(['CLUE', 'ANSWER', 'AUTHOR', 'EDITOR', 'LINK', 'DATE'])
            #scrape(writer, url)
            parse_crossword(url, f)

            print('Done with ' + date + "!")



if __name__ == '__main__':
    scraper()