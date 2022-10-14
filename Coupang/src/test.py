import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root',
                       password='0000', charset='utf8')
cursor = conn.cursor()
