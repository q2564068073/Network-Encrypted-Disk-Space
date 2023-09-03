#创建用户表，存储用户的基本信息
import pymysql
from pymysql import *
import config
def create_table():
    conn = connect(config.SERVER_DB)
    cursor = conn.cursor()
    create_users_table = """
    CREATE TABLE users (
        username VARCHAR(10) NOT NULL,
        password VARCHAR(50) NOT NULL,
        email VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        PRIMARY KEY (username)
    )
    """
    cursor.execute(create_users_table)

#对于每一个用户有一个特定的文件表，文件表存储文件名和特定存储文件的
    create_files_table = """
    CREATE TABLE files (
        username VARCHAR(10) NOT NULL,
        filename VARCHAR(100) NOT NULL,
        hash_value VARCHAR(100) NOT NULL,
        PRIMARY KEY (username, filename),
        FOREIGN KEY (username) REFERENCES users (username)
    )
    """

    cursor.execute(create_files_table)
    
    #提交
    conn.commit()
    cursor.close()
    conn.close()
