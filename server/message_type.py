import random
import urllib #发送请求
import hashlib #加密
import os
from flask import Flask
from config import *
import base64
import time
import socket
from sql_init import *

email_code_storage = {}
phone_code_storage = {}

#注册
def register(username, password, email, phone):
    #print("我进来了")
    sql_response = create_user(username, password, email, phone)
    #print("我出来了")
    if sql_response == 0:
        #print('用户已存在')
        return 0    #用户名已存在
        #返回注册界面
    elif sql_response == 1:
        #print('邮箱已存在')
        return 1 #邮箱已存在
        #返回注册界面
    elif sql_response==2:
        print('电话号码已存在')
        return 2
    else:#注册成功
        #make_folder(SERVER_PATH, username)#在指定目录创建用户文件夹
        #print('注册成功')
        return
        #返回使用界面

#用户密码登录
#如果用户不存在返回0 密码错误返回1 登录成功返回2
def login_password(username, password):
    sql_response = login_check_password(username, password)
    if sql_response == 0:
        return 0  #"用户名不存在"
        # 返回登录界面
    elif sql_response == 1:
        return 1  #"密码错误"
        # 返回登录界面
    elif sql_response == 2:
        return 2  #登录成功
        # 返回使用界面

####未完成
#向客户端指定的邮箱发送邮箱验证码
#如果邮箱不存在返回0 发送成功直接返回1
def get_email_code(email):
    AUTH_CODE = getrate_random()  #获取一个四位随机数
    sql_response = login_check_email(email)
    if sql_response == 0:
        return 0   #"邮箱不存在"
    elif sql_response == 1:
        email_message = str("【加密网盘】您的验证码为" + AUTH_CODE + "，30秒内有效。若非本人操作，请忽略此消息。")
        k=send_email(email, email_message)
        if k:
            print('发送成功')
        else:
            print('发送失败')
            return 2
        #把正确的email和验证码对应起来放在全局变量里面，等一下需要再次验证
        email_code_storage[email] = AUTH_CODE
        return 1

#判断邮箱和验证码是否正确
def login_email(email, auth_code):
    if email in email_code_storage:
        if auth_code == email_code_storage[email]:   #登陆成功
            return 2
            # 返回使用界面
        else:       #验证码不正确
            return 1
            # 返回登录界面
    else:
        return 0  
        #邮箱错误（如果在输入邮箱获得验证码之后把邮箱篡改掉，会提示错误）

#向客户端发送手机号验证码 0代表手机号不存在 1代表存在 发送成功
def get_phone_code(phone):
    AUTH_CODE = getrate_random()
    sql_response = login_check_phone(phone)
    if sql_response == 0: #手机号码不存在"
        return 0
    if sql_response == 1:
        send_phone(phone, AUTH_CODE)
        phone_code_storage[phone] = AUTH_CODE
        #验证码已发送
        return 1

#修改密码，如果验证码正确，就用新的密码去覆盖旧的密码
#修改成功返回2 确认密码不一样返回1 验证码不正确返回0
def change_password(phone, auth_code, password_1, password_2):
    if auth_code == phone_code_storage[phone]:
        if password_1 == password_2:
            change_my_password(phone,password_1)
            #"修改成功"
            return 2
        else:
            #"两次密码不一致"
            return 1
    else:
        #"验证码不正确"
        return 0


#获得四位随机数
def getrate_random():
    list1 = []
    for i in range(4):
        yan = random.randint(0, 9)
        list1.append(yan)
    return str(list1)

#md5加密
def md5s(strs):
    m = hashlib.md5()
    m.update(strs.encode("utf8")) #进行加密
    return m.hexdigest()

#给邮件发送验证码
def send_email(email, email_message):
    smtp_server = 'smtp.qq.com'  # 你的邮件服务器地址
    smtp_port = 25  # 邮件服务器端口号
    sender_email = '498618798@qq.com'  # 你的邮箱地址
    sender_password = 'ueaoenpgwgdgbjcg'  # 你的邮箱密码
    recipient_email=email
    subject = '验证码'

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((smtp_server, smtp_port))

            # 接收服务器返回的连接信息
            response = client_socket.recv(1024).decode()


            ehlo = "ehlo smtp.qq.com\r\n"
            client_socket.send(ehlo.encode())
            response = client_socket.recv(1024).decode()


            auth = f"auth login\r\n"
            client_socket.send(auth.encode())

            auth = f"{base64.b64encode(bytes(sender_email, 'utf-8')).decode('utf-8')}\r\n"
            client_socket.send(auth.encode())

            auth = f"{base64.b64encode(bytes(sender_password, 'utf-8')).decode('utf-8')}\r\n"
            client_socket.send(auth.encode())

            time.sleep(0.5)

            # 发送发件人信息
            mail_from_command = f'mail from: <{sender_email}>\r\n'
            client_socket.send(mail_from_command.encode())
            response = client_socket.recv(1024).decode()


            # 发送收件人信息
            rcpt_to_command = f'rcpt to: <{recipient_email}>\r\n'
            client_socket.send(rcpt_to_command.encode())
            response = client_socket.recv(1024).decode()


            # 发送数据命令
            data_command = 'data\r\n'
            client_socket.send(data_command.encode())

            From = f"From: <{sender_email}>\r\n"
            client_socket.send(From.encode())

            To = f"To: <{recipient_email}>\r\n"
            client_socket.send(To.encode())

            Subject = f"Subject: {subject}\r\n\r\n"
            client_socket.send(Subject.encode())

            Message = f"{email_message}\r\n"
            client_socket.send(Message.encode())

            end = ".\r\n"
            client_socket.send(end.encode())

            # 断开连接
            quit_command = 'QUIT\r\n'
            client_socket.send(quit_command.encode())
            response = client_socket.recv(1024).decode()

        return True
    except Exception as e:

        return False



#给特定的手机号发送验证码
def send_phone(phone, auth_code):
    sms_api = SMS_API
    # 短信平台账号
    sms_user = SMS_USER
    # 短信平台密码
    sms_password = md5s(SMS_PASSWORD)
    # 要发送的短信内容
    content = str("【加密网盘】您的验证码为" + auth_code + "，30秒内有效。若非本人操作，请忽略此消息。")
    # 要发送短信的手机号码
    data = urllib.parse.urlencode({'u': sms_user, 'p': sms_password, 'm': phone, 'c': content})  # 参数
    send_url = sms_api + 'sms?' + data  # 拼接url
    urllib.request.urlopen(send_url)  # 发送请求


def make_folder(path, folder_name):
    os.mkdir(path + folder_name)

def save_file(username, filename, data):
    try:
        if not os.path.isdir(f'../file/{username}'):
            make_folder('../file', username)
        else:
            with open(f'../file/{username}/{filename}', 'wb') as f:
                f.write(data)
            return True
    except Exception:
        return False

def send_file(username, filename, key_hash):
    try:
        # 查数据库校验hash
        
        with open(f'../file/{username}/{filename}', 'rb') as f:
            data = f.read()
            pass
        return True
    except Exception:
        return False