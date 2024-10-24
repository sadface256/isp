import requests
from bs4 import BeautifulSoup
import csv

def scrape(writer, url):
    url = url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    #soup = BeautifulSoup(open("C:/Users/swimm/Documents/isp/trying/crossword.html"), 'html.parser')
    author_editor = soup.find("div", {"class": "aegrid"}).text.strip().splitlines()
    link = soup.find("link", {"rel": "canonical"}).get('href')
    date = link.split("=")[1]
    #print(author_editor)
    author = author_editor[0].split(":")[1]
    editor = author_editor[1].split(":")[1]
    #print(author)
    #print(editor)
    #print(link)
    #print(date)
    clues = soup.find_all("div", {"class": "numclue"})
    for clues_list in clues:
        div_list = clues_list.find_all("div")
        for div in div_list:
            if ":" in div.text:
                clue_pair = div.text.split(":")
                clue = " ".join(clue_pair[:-1]).strip()
                #make the clue succinct, concatenate them
                answer = clue_pair[-1].strip()
                #print(clue, answer)
                row = [clue, answer, author, editor, link, date]
                #row = clue + ',' + answer + ',' + author + ',' + editor + ',' + link + ',' + date
                writer.writerow(row)
            #print(div.text)
            pass
    #print(clues)