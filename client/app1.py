from tkinter import *
from tkinter import messagebox
from personal_info_window import PersonalInfoWindow
from get_message import*
from config import *

import socket

client = socket.socket()  # 生成socket连接对象
ip_port = (SERVER_IP, SERVER_PORT)  # 地址和端口号
try:
    client.connect(ip_port)  # 连接
    print('服务器已连接')
except :
    print('服务器连接失败，请修改后重新运行!!')
    exit(0)

#登录部分已经全部调试完毕，首先还是没有响应的框，记得补一下
#问题：邮箱验证登录部分的验证码是   列表list形式！！！  和后端有关系，暂时没有解决！ 其余没问题了
def login():
  login_window = Toplevel(window)
  login_window.title("登录")
  login_window.geometry("400x400+420+0")

  login_method = login_method_variable.get()
  # 用户名登录
  if login_method == "username_password":
    username = StringVar()
    password = StringVar()
    Label(login_window, text="用户名：", font=("Arial", 14)).pack()
    Entry(login_window, font=("Arial", 14),textvariable=username).pack()

    Label(login_window, text="密码：", font=("Arial", 14)).pack()
    Entry(login_window, show="*", font=("Arial", 14),textvariable=password).pack()

    def login_by_username():
      loginname = LoginName()
      message = loginname.get_message(username.get(),password.get())
      send_message(client, message)
      print(message)
      flag = receive_message(client)
      print(flag)
      if flag == '0':  # 用户名不存在
        messagebox.showerror("登录失败", "用户名不存在！")
      elif flag == '1':  # 密码错误
        messagebox.showerror("登录失败", "密码错误！")
      elif flag == '2':  # 登录成功
        messagebox.showinfo("登录成功", "登录成功！")
        PersonalInfoWindow(username.get(),client)
        # 弹出用户页面

    Button(login_window, text="登录", font=("Arial", 14),command=login_by_username).pack()

  # 邮箱登录
  elif login_method == "email_code":
    email = StringVar()
    email_code = StringVar()

    Label(login_window, text="邮箱：", font=("Arial", 14)).pack()
    Entry(login_window, font=("Arial", 14), textvariable=email).pack()

    Label(login_window, text="验证码：", font=("Arial", 14)).pack()
    Entry(login_window, font=("Arial", 14), textvariable=email_code).pack()

    # 需要监听获取点击获取邮箱验证码的事件信息并传输
    def get_email_verification_code():
      get_email_verification_code = GetEmailVerificationCode()
      message = get_email_verification_code.get_message(email.get())
      send_message(client, message)
      print(message)
      flag = receive_message(client)
      print(flag)
      # 反馈信息
      if flag == '0':
        messagebox.showerror("发送失败", "邮箱不存在！")
      elif flag == '1':
        messagebox.showinfo("发送成功", "验证码已发送！")
    Button(login_window, text="获取验证码", font=("Arial", 14),command=get_email_verification_code).pack()

    def login_by_email():
      loginemail = LoginEmail()
      #message = loginemail.get_message(email.get(), email_code.get())
      message = loginemail.get_message(email.get(), email_code.get())
      send_message(client, message)
      flag = receive_message(client)
      print(flag)
      if flag == '0':
        messagebox.showerror("登录失败", "邮箱错误！")
      elif flag == '1':
        messagebox.showishowerrornfo("登录失败", "验证码错误！")
      elif flag == '2':
        messagebox.showinfo("登录成功", "登录成功！")
        '''
        最好是使用服务器根据数据库查询到的邮箱匹配的姓名，返回的username
        '''
        PersonalInfoWindow('邮箱匹配的姓名',client)
        # 跳转使用界面

    Button(login_window, text="登录", font=("Arial", 14), command=login_by_email).pack()

#注册功能调试完毕
#注册的结果好像还没有响应框（成功失败）
#邮箱和手机号格式检查部分需要改一下 还有响应框
def register():
  register_window = Toplevel(window)
  register_window.title("注册")
  register_window.geometry("400x400+840+0")

  # 创建四个StringVar变量
  username = StringVar()
  password = StringVar()
  email = StringVar()
  phone_number = StringVar()
  # 创建用户名输入框
  Label(register_window, text="用户名：", font=("Arial", 14)).pack()
  Entry(register_window, font=("Arial", 14), textvariable=username).pack()

  # 创建密码输入框
  Label(register_window, text="密码：", font=("Arial", 14)).pack()
  Entry(register_window, show="*", font=("Arial", 14), textvariable=password).pack()
  # 创建邮箱输入框
  Label(register_window, text="邮箱：", font=("Arial", 14)).pack()
  Entry(register_window, font=("Arial", 14), textvariable=email).pack()
  # 创建电话号码输入框
  Label(register_window, text="电话号码：", font=("Arial", 14)).pack()
  Entry(register_window, font=("Arial", 14), textvariable=phone_number).pack()


  def register_user():
    registration = Registration()
    message = registration.get_message(username.get(), password.get(), email.get(), phone_number.get())
    print(message)
    if message == "格式错误":
      messagebox.showerror("格式错误","请输入正确的信息")
    else:
      send_message(client, message)
      flag = receive_message(client)
      #print("逆天")
      print(flag)        #注册的结果应该有对应的框，此处好像没有看到
      if flag == '0':
        messagebox.showerror("注册失败", "用户名已存在！")
      elif flag == '1':
        messagebox.showerror("注册失败", "邮箱已存在！")
      elif flag == '2':
        messagebox.showinfo("注册成功", "注册成功！")
        PersonalInfoWindow(username.get(),client)     
        # 跳转使用界面
  # 创建注册按钮，并在点击时调用register_user方法
  Button(register_window, text="注册", font=("Arial", 14), command=register_user).pack()

#忘记密码部分需要注意一下返回值，在给手机发送完验证码之后可以修改密码
#如果前后两次密码不一样，此处的FALSE返回值改一下
def forgot_password():
  forgot_password_window = Toplevel(window)
  forgot_password_window.title("忘记密码")
  forgot_password_window.geometry("400x400+840+0")

  phone_number = StringVar()
  phone_code = StringVar()
  new_password1 = StringVar()
  new_password2 = StringVar()
  Label(forgot_password_window, text="手机号：", font=("Arial", 14)).pack()
  Entry(forgot_password_window, font=("Arial", 14),textvariable=phone_number).pack()

  Label(forgot_password_window, text="验证码：", font=("Arial", 14)).pack()
  Entry(forgot_password_window, font=("Arial", 14),textvariable=phone_code).pack()

  # 需要监听获取点击获取手机验证码的事件信息并传输
  def get_phone_verification_code():
    get_phone_verification_code = GetPhoneVerificationCode()
    message = get_phone_verification_code.get_message(phone_number.get())
    send_message(client, message)
    print(message)
    flag = receive_message(client)
    print(flag)
    # 反馈信息
    if flag == '0':
      messagebox.showerror("发送失败", "手机号不存在！")
    elif flag == '1':
      messagebox.showinfo("发送成功", "验证码已发送！")
  Button(forgot_password_window, text="获取验证码", font=("Arial", 14),command=get_phone_verification_code).pack()

  Label(forgot_password_window, text="新密码：", font=("Arial", 14)).pack()
  Entry(forgot_password_window, show="*", font=("Arial", 14),textvariable=new_password1).pack()

  Label(forgot_password_window, text="确认密码：", font=("Arial", 14)).pack()
  Entry(forgot_password_window, show="*", font=("Arial", 14),textvariable=new_password2).pack()

  def forget_password():
    forgetpassword = ForgetPassword()
    message = forgetpassword.get_message(phone_number.get(),phone_code.get(),new_password1.get(),new_password2.get())
    send_message(client, message)
    print(message)
    flag = receive_message(client)
    print(flag)
    if flag == '0':
      messagebox.showerror("修改失败", "验证码不正确！")
    elif flag == '1':
      messagebox.showerror("修改失败", "两次密码不一致！")
    elif flag == '2':
      messagebox.showinfo("修改成功", "修改成功！")
  Button(forgot_password_window, text="确认修改", font=("Arial", 14),command=forget_password).pack()

#发送消息
def send_message(client,message):
  client.send(message.encode())

#接收消息，返回接收到的字符串
def receive_message(client):
  response = "$"
  while response == "$":
    response = client.recv(1024).decode()
  return response


# 创建窗口
window = Tk()
window.title("登录注册系统")
# 设置窗口大小和位置
window.geometry("400x400+0+0")
window.resizable(False, False)



# 创建登录方式选择框
login_method_label = Label(window, text="登录方式:", font=("Arial", 12))
login_method_label.pack(pady=10)

login_method_variable = StringVar()
login_method_variable.set("username_password")
username_password_radio = Radiobutton(window, text="用户名+密码", variable=login_method_variable, value="username_password", font=("Arial", 12))
username_password_radio.pack()

email_code_radio = Radiobutton(window, text="邮箱+验证码", variable=login_method_variable, value="email_code", font=("Arial", 12))
email_code_radio.pack()

# 创建登录和注册按钮
login_button = Button(window, text="登录", command=login, font=("Arial", 14), width=20)
login_button.pack(pady=10)

register_button = Button(window, text="注册", command=register, font=("Arial", 14), width=20)
register_button.pack(pady=10)

# 创建忘记密码按钮
forgot_password_button = Button(window, text="忘记密码", command=forgot_password, font=("Arial", 14), width=20)
forgot_password_button.pack(pady=10)

# 进入主循环
window.mainloop()
