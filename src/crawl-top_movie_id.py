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
sql_insert_mvid = """INSERT IGNORE INTO top_movie_table (movie_id) VALUES (%s)"""
db.ping(reconnect=True)

URL = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

driver = webdriver.Chrome(executable_path=r"C:\Users\quang\working_space\ScrapyIMDB\Browser\chromedriver.exe")
wait = WebDriverWait(driver, 10)

driver.get(URL)
soup = BeautifulSoup(driver.page_source, 'lxml')

for elem in soup.find_all(class_='titleColumn'):
  movie_link = elem.a.get('href')
  movie_id = movie_link.split('/')[2]
  print('get movie_id',movie_id)
  cursor.execute(sql_insert_mvid, (movie_id,))
  db.commit()


driver.quit()
cursor.close()
db.close()
