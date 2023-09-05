import random
import socket
import base64
import urllib #发送请求
import hashlib #加密
import os
import time
from flask import Flask
from config import *
from sql_init import *

email_code_storage = {}
phone_code_storage = {}
username_storage = {}

#注册
def register(username, password, email, phone):
    #print("我进来了")
    sql_response = create_user(username, password, email, phone)
    #print("我出来了")
    if sql_response == 0:
        #print('用户名已存在')
        return 0    #用户名已存在
        #返回注册界面
    elif sql_response == 1:
        #print('邮箱已存在')
        return 1 #邮箱已存在
        #返回注册界面
    else:#注册成功
        #make_folder(SERVER_PATH, username)#在指定目录创建用户文件夹
        #print('注册成功')
        return 2
        #返回使用界面

#用户密码登录
#如果用户不存在返回0 密码错误返回1 登录成功返回2
def login_password(username, password):
    #print("我进来了")
    sql_response = login_check_password(username, password)
    #print("我出来了")
    if sql_response == 0:
        return 0  #"用户名不存在"
        # 返回登录界面
    elif sql_response == 1:
        return 1  #"密码错误"
        # 返回登录界面
    elif sql_response == 2:
        return 2  #登录成功
        # 返回使用界面

#向客户端指定的邮箱发送邮箱验证码
#如果邮箱不存在返回0 发送成功直接返回1
def get_email_code(email):
    AUTH_CODE = getrate_random() #获取一个四位随机数
    print(AUTH_CODE)
    #此处生成的随机数是以字典形式呈现的 比如[2,2,4,2]
    #此处尝试把字典转换为数字，但是转换之后会出现问题
    #在编辑发送给服务器的消息时，验证码要以字典的形式组装
    sql_response = login_check_email(email)
    if sql_response == 0:
        return 0   #"邮箱不存在"
    else:
        email_message = str("【加密网盘】您的验证码为" + AUTH_CODE + "，30秒内有效。若非本人操作，请忽略此消息。")
        send_email(email, email_message)
        #把正确的email和验证码对应起来放在全局变量里面，等一下需要再次验证
        email_code_storage[email] = AUTH_CODE
        username_storage[email] = sql_response
        return 1  #发送成功

#判断邮箱和验证码是否正确
#登录逻辑：首先开启服务器激活全局变量email_code_storage从而开始储存，如果点击获取验证码之后
#关闭服务器的话，那么此前获得的验证码将无效，需要重新获得验证码
#此处需要测试！！！ 如果获得验证码之后关闭客户端能不能正常运行
def login_email(email, auth_code):
    if email in email_code_storage:
        if auth_code == email_code_storage[email]:   #登陆成功
            return username_storage[email]
        else:       #验证码不正确
            return 1
    else:
        return 0  
        #邮箱错误（如果在输入邮箱获得验证码之后把邮箱篡改掉，会提示错误）

#向客户端发送手机号验证码 0代表手机号不存在 1代表存在 发送成功
def get_phone_code(phone):
    AUTH_CODE = getrate_random()
    print(AUTH_CODE)
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

'''
#获得四位随机数
def getrate_random():
    number = 0
    for i in range(4):
        digit = random.randint(0,9)
        number = number * 10 + digit
    return number
'''
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
    smtp_server = SMTP_SERVER  # 你的邮件服务器地址
    smtp_port = SMTP_PORT  # 邮件服务器端口号
    sender_email = SENDER_EMAIL  # 你的邮箱地址
    sender_password = SENDER_PASSWORD  # 你的邮箱密码
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

<<<<<<< HEAD
'''
# 存储共享空间的字典，每个共享空间包含成员和文件
shared_spaces = {}
def create_shared_space(username,space_name):
    shared_spaces[space_name] = {'members': set(), 'files': {}}
    add_user_to_shared_space(username,space_name)
    return f"共享空间 '{space_name}' 创建成功"
    
def add_user_to_shared_space(username, space_name):
    k=check_username(username)
    if k==1 and space_name in shared_spaces:
=======
# 存储共享空间的字典，每个共享空间包含成员和文件
shared_spaces = {}
def create_shared_space(username,space_name):
    shared_spaces[space_name] = {'members': set()}
    if not os.path.isdir(f'../file/space/{space_name}'):
        make_folder('../file/space', space_name)
    add_user_to_shared_space(username,space_name)
    return f"共享空间 '{space_name}' 创建成功"

def add_user_to_shared_space(username, space_name):
    if  space_name in shared_spaces and username in shared_spaces[space_name]['members']:
>>>>>>> 527f623bbc073b1073210cc0c53a79deb8eff66c
        shared_spaces[space_name]['members'].add(username)
        return f"用户 '{username}' 已加入共享空间 '{space_name}'"
    else:
        return "用户或共享空间不存在"
<<<<<<< HEAD
'''
=======
>>>>>>> 527f623bbc073b1073210cc0c53a79deb8eff66c

def make_folder(path, folder_name):
    os.mkdir(path + './'+folder_name)
    
#检查是否有重复文件，如果没有才允许上传
def save_file_check(username,filename,key_hash):
    k = insert_file(username,filename,key_hash)
    if k == 0:
        return 0
    elif k == 2:
        return 'ok'

#把文件保存到指定路径的位置里面去 
def save_file(username, filename, data):
    try:
        '''
        k=insert_file(username,filename,key_hash) 
        # 这个需要补充
        # 先入表 返回0是已经上传过 返回1是未上传 可以进行上传
        #k=1
        if k==0:
            return False
        '''
        # project_folder/
        #├── script_folder/
        #│       └── your_script.py
        #└── file/
        #       └── orangestar/
        # 如上 在本script的上级的同级file文件夹中建立新的文件夹 可以根据需求改存储路径
        # 先拼接路径

        project_directory = os.path.dirname(os.path.dirname(__file__))
        new_folder_name = username
        new_folder_path = os.path.join(project_directory, 'file', new_folder_name)

        # 拼接好路径后 进行创建
        if not os.path.isdir(new_folder_path):
            #make_folder('../file', username)
            os.makedirs(new_folder_path)
        # 创建后开始写文件 写到orangestar/中
        with open(f'{new_folder_path}/{filename}', 'wb') as f:
            f.write(data)
        return True
    
    except Exception:
        return False

#在数据库里面找到指定用户的文件
#此处的k注意显示
def find_file(username):
    k=find(username)
    if k==0:
        return 0
    else:
        return k

'''
def send_file(username, filename, key_hash, client_socket):
    try:
        k=get_file(username,filename,key_hash)
        if k==1:
            print('解压密码错误')
            return False
        elif k==0:
            print('文件不存在')
        else:
            with open(f'../file/{username}/{filename}', 'rb') as f:
                data = f.read()
                es = EncryptedSocket(client_socket)
                es.send_encrypt(data)
            return True
    except Exception:
        return False

def find_file(username,client_socket):
    try:
        k=find(username)
        if k==1:
            print("该用户没有文件")
            return False
        else:
            es = EncryptedSocket(client_socket)
            es.send_encrypt(k)
            return True
    except Exception:
        return False

def save_qfile(spacename,filename,data):
    try:
        directory_path=f'../file/space/{spacename}'
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            print('文件已存在于共享空间')
            return False
        else:
            with open(f'../file/space/{spacename}/{filename}', 'wb') as f:
                f.write(data)
            return True
    except Exception:
        return False
'''
