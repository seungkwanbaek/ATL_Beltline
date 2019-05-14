import pymysql.cursors


def create_connection():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='mysql',
                           db='cs4400_team70',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
