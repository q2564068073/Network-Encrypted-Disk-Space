conn = pymysql.connect(
    host=SERVER_DB['host'],
    user=SERVER_DB['user'],
    password=SERVER_DB['password'],
    database=SERVER_DB['database'],
    charset=SERVER_DB['charset']
)