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
# create top_movie_table
sql = """CREATE TABLE top_movie_id_table_test (
   movie_id CHAR(20) PRIMARY KEY,
   movie_id_isCrawled int
)"""
db.ping(reconnect=True)

cursor.execute(sql)
# result = cursor.fetchall()
# # print(result)
# for index, id in enumerate(result):
#     (uid,) = id
#     print(uid)



cursor.close()
db.close()
