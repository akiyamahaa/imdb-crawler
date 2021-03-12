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
sql = """CREATE TABLE rating_multi_table (
   user_id CHAR(20),
   movie_id CHAR(20),
   rating int,
   timestamp int
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
