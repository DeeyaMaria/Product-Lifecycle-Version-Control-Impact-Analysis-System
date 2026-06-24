import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="versionforge",
    cursorclass=pymysql.cursors.Cursor
)

cursor = conn.cursor()