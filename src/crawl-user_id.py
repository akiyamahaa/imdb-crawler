from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
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
sql_insert_uid = """INSERT IGNORE INTO user_table (iduser) VALUES (%s)"""
sql_get_mvid = """SELECT * FROM top_movie_id_table"""
sql_confirm_crawled = """UPDATE top_movie_id_table SET movie_id_isCrawled = 1 WHERE movie_id = %s"""


db.ping(reconnect=True)

driver = webdriver.Chrome(executable_path=r"C:\Users\quang\working_space\ScrapyIMDB\Browser\chromedriver.exe")
wait = WebDriverWait(driver, 10)

def get_user_id(soup, movie_id):
    while True:
        try:
            driver.find_element_by_css_selector("button#load-more-trigger").click()
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".ipl-load-more__load-indicator")))
            soup = BeautifulSoup(driver.page_source, 'lxml')
        except Exception:
            break
    for elem in soup.find_all(class_='imdb-user-review'):
        user_link = elem.find(class_='display-name-link').a.get('href')
        uid = user_link.split('/')[2]
        user_rating_link = elem.find(class_='rating-other-user-rating')
        if user_rating_link:
            print('Get UID',uid)
            cursor.execute(sql_insert_uid, (uid,))
            cursor.execute(sql_confirm_crawled, (movie_id,))
            db.commit()

# get movie id
cursor.execute(sql_get_mvid)
result = cursor.fetchall()
for index, packs in enumerate(result):
    (movie_id,movie_isCrawled) = packs
    if movie_isCrawled == 0:
        print('Crawl with movie ', movie_id)
        movie_page_url = "https://www.imdb.com/title/" + movie_id +"/reviews?sort=userRating&dir=desc&ratingFilter=0"
        driver.get(movie_page_url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        get_user_id(soup,movie_id)
    else:
        print('Movie is crawled',movie_id)

driver.quit()
cursor.close()
db.close()
