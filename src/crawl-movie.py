import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

CSV_FILE = '../test_movie.csv'
csvFile = pd.read_csv(CSV_FILE)

driver = webdriver.Chrome(executable_path=r"C:\Users\quang\working_space\ScrapyIMDB\Browser\chromedriver.exe")
wait = WebDriverWait(driver, 10)

def find_cast_or_crew(type):
    type_list = []
    if type != 'cast':
        type_list_link = soup.select_one('#'+type).findNext('table').find_all(class_='name')
        for elem in type_list_link:
            if elem.get_text(strip=True) not in type_list:
                type_list.append(elem.get_text(strip=True))
    else:
        type_list_link = soup.select_one('#'+type).findNext('table').find_all(class_='primary_photo')
        for elem in type_list_link:
            if elem.findNext('td').get_text(strip=True) not in type_list:
                type_list.append(elem.findNext('td').get_text(strip=True))
    return type_list

for index, movieid in enumerate(csvFile['movieid']):
    print('Processing in Movie...',movieid)
    movie_url = 'https://www.imdb.com/title/' + movieid
    movie_fullcredits_url = 'https://www.imdb.com/title/' + movieid + '/fullcredits/'
    # Get Infomartion Movie
    driver.get(movie_url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    movie_name = soup.find(class_='title_wrapper').find('h1').get_text(strip=True)
    movie_runtime = soup.find(class_='subtext').find('time').get_text(strip=True)
    movie_genres_link = soup.find(lambda tag: tag.name == "h4" and "Genres" in tag.text).findNextSiblings('a')
    movie_genres = []
    for each_genres in movie_genres_link:
        movie_genres.append(each_genres.get_text(strip=True))
    movie_avg_rating = soup.find(itemprop='ratingValue').get_text(strip=True)
    movie_votes = soup.find(itemprop='ratingCount').get_text(strip=True)

    # Get FullCredit
    driver.get(movie_fullcredits_url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    director_list = find_cast_or_crew('director')
    writers_list = find_cast_or_crew('writer')
    cast_list = find_cast_or_crew('cast')
    print(director_list)
    print(writers_list)
    print(cast_list)

driver.quit()
