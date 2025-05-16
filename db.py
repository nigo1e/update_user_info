import pymysql
def get_conn():
    return pymysql.connect(
        host='82.157.178.120',
        user='test123456',
        password='123456',
        database='wx_hongniang',
        port=3306,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.Cursor
    )