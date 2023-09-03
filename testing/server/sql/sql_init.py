"""
定义数据库操作的各种函数
"""

from pymysql import *
from pprint import pprint
import config

#用户注册的功能，检查用户是否已经存在了，如果用户不存在的话那就注册
#用户名已存在返回0 邮箱已经存在返回1 注册成功返回2
def create_user(username,password,email,phone):
    conn = connect(config.SERVER_DB)
    cursor = conn.cursor()
    
    #检查用户名是否已经存在了 如果已经存在直接return 0
    cursor.execute("SELECT * FROM users WHERE username=?",(username,))
    if cursor.fetchone() is not None:
        #用户名已存在
        conn.close()
        return 0  
    
    #检查邮箱是不是已经存在了 如果存在也不允许注册
    cursor.execute("SELECT * FROM users WHERE email=?",(email,))
    if cursor.fetchone() is not None:
        conn.close()
        return 1
    
    #插入新用户信息
    cursor.execute("INSERT INTO users (username,password,email,phone) VALUES (?,?,?,?)",(username,password,email,phone))
    conn.commit()
    
    #注册成功
    conn.close()
    return 2

#登录方式1：通过用户密码登录
def login_check_password(username,password):
    conn = connect(config.SERVER_DB)
    cursor = conn.cursor()
    
    #检查用户名存在情况
    cursor.execute("SELECT * FROM users WHERE username=?",(username,))
    user = cursor.fetchone() #这里的user是一个完整的查询结果，(username,password,...)
    if user is None:
        #用户名是不存在的，要提醒一下没有这个人
        conn.close()
        return 0
    else:  
        stored_password = user[1] #按照数组的顺序
        
        if password == stored_password:
            conn.close()
            return 2 #这里是登录成功了，记得给一个返回值
        else:
            conn.close()
            return 1 #这里是密码错误了，记得返回登录失败
    

#登录方式2：通过邮箱和验证码登录
def login_check_email(email):
    conn = connect(config.SERVER_DB)
    cursor = conn.cursor()
    
    #检查邮箱存在的情况
    cursor.execute("SELECT * FROM users WHERE email=?",(email,))
    if cursor.fetchone() is None:
        #这里的话邮箱不存在，登录失败了
        conn.close()
        return 0
    else:
        #这里代表可以登录，需要发送一个邮箱验证码来验证
        conn.close()
        return 1
        
#检查手机号是否存在于数据库里面
def login_check_phone(phone):
    conn = connect(config.SERVER_DB)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE phone=?",(phone,))
    if cursor.fetchone() is None:
        conn.close()
        return 0  #不存在
    else:
        conn.close()
        return 1   #存在于数据库中

#修改密码,用新密码覆盖原密码
def change_my_password(phone,new_password):
    conn = connect(config.SERVER_DB)
    cursor = conn.cursor()
    
    update_query = "UPDATE your_table SET password = ? WHERE phone = ?"
    cursor.execute(update_query, (new_password,phone))

    # 提交事务并关闭连接
    conn.commit()
    conn.close()