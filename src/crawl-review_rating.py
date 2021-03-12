from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from dateutil.parser import parse
import time
from datetime import datetime

import pymysql

db = pymysql.connect(
    user='root',
    password='1234',
    host='localhost',
    database='imdb',
    port=3306,
    charset="utf8"
)
cursor = db.cursor()
db.ping(reconnect=True)
sql_get_uid = """SELECT * FROM user_table"""
sql_put_data = """REPLACE INTO rating_table (user_id,movie_id,rating,timestamp) VALUES (%s,%s,%s,%s)"""
sql_remove_uid = """DELETE FROM user_table WHERE iduser = %s"""
sql_check_crawled_uid = """SELECT EXISTS(
	SELECT * FROM rating_table
	where user_id = %s
    )"""
driver = webdriver.Chrome(executable_path=r"C:\Users\quang\working_space\ScrapyIMDB\Browser\chromedriver.exe")
wait = WebDriverWait(driver, 10)


def get_info_review_rating(soup, uid):
    print('Process for user....', uid)
    for elem in soup.find_all(class_='mode-detail'):
        movie_titleId_link = elem.find(class_='lister-item-header').a.get('href')
        # info movie
        movie_id = movie_titleId_link.split('/')[2]
        movie_user_rating = elem.find(class_='ipl-rating-star--other-user')
        if movie_user_rating is not None:
            movie_user_rating = elem.find(class_='ipl-rating-star--other-user').find('span',
                                                                                     class_='ipl-rating-star__rating').get_text(
                strip=True)

            for t in elem.select('.ipl-rating-widget + p'):
                movie_timestamp = t.text
            movie_timestamp = movie_timestamp[9:20]
            movie_timestamp = parse(movie_timestamp).date()
            movie_timestamp = time.mktime(datetime.strptime(str(movie_timestamp), "%Y-%m-%d").timetuple())
            cursor.execute(sql_put_data, (uid, movie_id, movie_user_rating, movie_timestamp))
            db.commit()


def get_user_rating_page(user_rating_url, uid):
    driver.get(user_rating_url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    button_next = soup.find('a', class_='lister-page-next')
    get_info_review_rating(soup, uid)
    while button_next is not None:
        try:
            driver.find_element_by_css_selector("a.lister-page-next").click()
            soup = BeautifulSoup(driver.page_source, 'lxml')
            get_info_review_rating(soup, uid)
            button_next = soup.find('a', class_='lister-page-next')
        except Exception:
            break


# get user id
cursor.execute(sql_get_uid)
result = cursor.fetchall()
for index, id in enumerate(result):
    (uid,) = id
    # check exist uid in db
    cursor.execute(sql_check_crawled_uid,(uid,))
    result = cursor.fetchall()
    ((result,),) = result
    # if not crawled, result = 0, otherwise != 0
    if result == 0:
        print('START WITH USER ...', uid)
        user_page_url = 'https://www.imdb.com/user/' + uid
        user_rating_url = 'https://www.imdb.com/user/' + uid + '/ratings'
        driver.get(user_page_url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        user_rating_available = soup.select_one('div.aux-content-widget-2 a[href]').get_text(strip=True)
        if user_rating_available == 'Ratings':
            get_user_rating_page(user_rating_url, uid)
        else:
            cursor.execute(sql_remove_uid, (uid,))
            db.commit()
            print('UID DELETED SUCCESSFULLY', uid)
    else:
        print('UID IS CRAWLED',uid)

driver.quit()
db.close()
