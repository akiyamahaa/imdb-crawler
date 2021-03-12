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
sql_insert_uid = """INSERT IGNORE INTO user_table (iduser) VALUES ('%s')"""
db.ping(reconnect=True)

URL = "https://www.imdb.com/title/tt0111161/reviews?sort=userRating&dir=desc&ratingFilter=0"
# URL = "https://www.imdb.com/title/tt0270846/reviews?sort=userRating&dir=desc&ratingFilter=0"

driver = webdriver.Chrome(executable_path=r"C:\Users\quang\working_space\ScrapyIMDB\Browser\chromedriver.exe")
wait = WebDriverWait(driver, 10)

driver.get(URL)
soup = BeautifulSoup(driver.page_source, 'lxml')

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
        print('Get Uid',uid)
        cursor.execute(sql_insert_uid,(uid,))
        db.commit()

driver.quit()
cursor.close()
db.close()
