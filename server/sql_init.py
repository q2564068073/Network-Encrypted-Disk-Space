"""
定义数据库操作的各种函数
"""

import pymysql
from pprint import pprint
from config import *
#用户注册的功能，检查用户是否已经存在了，如果用户不存在的话那就注册
#用户名已存在返回0 邮箱已经存在返回1 注册成功返回2
def create_user(username,password,email,phone):
    conn = pymysql.connect(
    host=SERVER_DB['host'],
    user=SERVER_DB['user'],
    password=SERVER_DB['password'],
    database=SERVER_DB['database'],
    charset=SERVER_DB['charset']
    )
    print("连接可以了")
    try:
        cursor = conn.cursor()
        #检查用户名是否已经存在了 如果已经存在直接return 0
        cursor.execute("SELECT * FROM users WHERE username=%s",(username,))
        if cursor.fetchone() is not None:
            #用户名已存在
            #conn.close()
            return 0  
        
        #检查邮箱是不是已经存在了 如果存在也不允许注册
        cursor.execute("SELECT * FROM users WHERE email=%s",(email,))
        if cursor.fetchone() is not None:
            #conn.close()
            return 1
        
        #插入新用户信息
        cursor.execute("INSERT INTO users (username,password,email,phone) VALUES (%s,%s,%s,%s)",(username,password,email,phone))
        conn.commit()
        #注册成功
        return 2
    except Exception as e:
        # 发生异常时记录错误日志或返回错误信息
        print("Error:", e)
        return -1
    finally:
        # 关闭数据库连接
        conn.close()
        
#登录方式1：通过用户密码登录
def login_check_password(username,password):
    conn = pymysql.connect(
    host=SERVER_DB['host'],
    user=SERVER_DB['user'],
    password=SERVER_DB['password'],
    database=SERVER_DB['database'],
    charset=SERVER_DB['charset']
    )
    #print("连接可以了")
    #检查用户名存在情况
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s",(username,))
        user = cursor.fetchone() #这里的user是一个完整的查询结果，(username,password,...)
        if user is None:
            #用户名是不存在的，要提醒一下没有这个人
            #conn.close()
            return 0
        else:  
            stored_password = user[1] #按照数组的顺序
            
            if password == stored_password:
                #conn.close()
                return 2 #这里是登录成功了，记得给一个返回值
            else:
                #conn.close()
                return 1 #这里是密码错误了，记得返回登录失败
    except Exception as e:
        print("Error:",e)
        return -1
    finally:
        conn.close()

#登录方式2：通过邮箱和验证码登录
#登录之后返回用户名
def login_check_email(email):
    conn = pymysql.connect(
    host=SERVER_DB['host'],
    user=SERVER_DB['user'],
    password=SERVER_DB['password'],
    database=SERVER_DB['database'],
    charset=SERVER_DB['charset']
    )
    cursor = conn.cursor()
    
    try:
        #检查邮箱存在的情况
        cursor.execute("SELECT username FROM users WHERE email=%s",(email,))
        select_result = cursor.fetchone()
        if select_result is None:
            #这里的话邮箱不存在，登录失败了
            #conn.close()
            return 0
        else:
            #这里代表可以登录，需要发送一个邮箱验证码来验证
            #conn.close()
            return str(select_result)
    except Exception as e:
        print("Error:",e)
        return -1
    finally:
        conn.close()
        
#检查手机号是否存在于数据库里面
def login_check_phone(phone):
    conn = pymysql.connect(
    host=SERVER_DB['host'],
    user=SERVER_DB['user'],
    password=SERVER_DB['password'],
    database=SERVER_DB['database'],
    charset=SERVER_DB['charset']
    )
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE phone=%s",(phone,))
        if cursor.fetchone() is None:
            #conn.close()
            return 0  #不存在
        else:
            #conn.close()
            return 1   #存在于数据库中
    except Exception as e:
        print("Error:",e)
        return -1
    finally:
        conn.close()

#修改密码,用新密码覆盖原密码
def change_my_password(phone,new_password):
    conn = pymysql.connect(
    host=SERVER_DB['host'],
    user=SERVER_DB['user'],
    password=SERVER_DB['password'],
    database=SERVER_DB['database'],
    charset=SERVER_DB['charset']
    )
    cursor = conn.cursor()
    try:
        update_query = "UPDATE users SET password = %s WHERE phone = %s"
        cursor.execute(update_query, (new_password,phone))

        # 提交事务并关闭连接
        conn.commit()
        #conn.close()
    
    except Exception as e:
        print("Error:",e)
        return -1
    finally:
        conn.close()

#向服务器插入文件，如果文件已存在返回0，插入成功返回2
def insert_file(username,filename,hash_value):
    conn = pymysql.connect(
        host=SERVER_DB['host'],
        user=SERVER_DB['user'],
        password=SERVER_DB['password'],
        database=SERVER_DB['database'],
        charset=SERVER_DB['charset']
    )
    try:
        cursor = conn.cursor()
        # 检查文件名是否已经存在了 如果已经存在直接return 0
        cursor.execute("SELECT * FROM files WHERE username=%s and filename=%s", (username,filename))
        if cursor.fetchone() is not None:
            # 该文件已存在
            # conn.close()
            return 0

        # 插入新文件信息
        cursor.execute("INSERT INTO files (username,filename,hash_value) VALUES (%s,%s,%s)",(username,filename,hash_value))
        conn.commit()
        # 插入成功
        return 2
    except Exception as e:
        print("Error:", e)
        return -1
    finally:
        conn.close()

#在数据库里面根据指定的用户名找到其拥有的文件   
def find(username):
    conn = pymysql.connect(
        host=SERVER_DB['host'],
        user=SERVER_DB['user'],
        password=SERVER_DB['password'],
        database=SERVER_DB['database'],
        charset=SERVER_DB['charset']
    )
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT filename FROM files WHERE username=%s ", (username,))
        if cursor.fetchone() is not None:
            results = []
            for row in cursor.fetchall():  #fetchall 返回所有符合条件的表项
                filename = row[0]
                results.append(filename)
                return results
        else:  #如果没有对应的文件的话返回False
            #conn.commit()
            return False
    except Exception as e:
        print("Error:", e)
        return -1
    finally:
        conn.close()

        
def get_file(username, filename, hash_value):
    conn = pymysql.connect(
        host=SERVER_DB['host'],
        user=SERVER_DB['user'],
        password=SERVER_DB['password'],
        database=SERVER_DB['database'],
        charset=SERVER_DB['charset']
    )
    try:
        cursor = conn.cursor()
        # 检查文件名是否已经存在 如果已经存在直接return 0
        cursor.execute("SELECT hash_valse FROM files WHERE username=%s and filename=%s", (username, filename))
        if cursor.fetchone() is not None:
            if cursor.fetchone()==hash_value:
                #conn.conmmit()
                return 2
            # 获得权限下载
            else:
                #conn.commit()
                return 1
            # 文件解压密码不正确（没有权限）
        else:
            #conn.commit()
            return 0
        # 不存在该文件
    except Exception as e:
        print("Error:", e)
        return -1
    finally:
        conn.close()

def find (username):
    conn = pymysql.connect(
        host=SERVER_DB['host'],
        user=SERVER_DB['user'],
        password=SERVER_DB['password'],
        database=SERVER_DB['database'],
        charset=SERVER_DB['charset']
    )
    try:
        cursor = conn.cursor()
        # 检查文件名是否已经存在 如果已经存在直接return 0
        cursor.execute("SELECT filename FROM files WHERE username=%s ", (username,))
        if cursor.fetchone() is not None:
            results = []
            for row in cursor.fetchall():
                filename = row[0]
                results.append(filename)
                return results
        else:
            conn.commit()
            return 1
    except Exception as e:
        print("Error:", e)
        return -1
    finally:
        conn.close()

