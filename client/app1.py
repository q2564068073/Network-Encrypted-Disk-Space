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


def login():
  login_window = Toplevel(window)
  login_window.title("登录")
  login_window.geometry("500x500")

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
      client.send(message.encode())
      print (message)
      # flag = loginname.get_message(username.get(),password.get())
      # flag表示服务器关于用户名登录检测返回的结果，用client.receive接收
      flag = True
      if flag:
        messagebox.showinfo('用户名登陆成功！')
        # 登陆成功，进入个人主页
        PersonalInfoWindow(username)
      else:
        messagebox.showinfo('用户名登陆失败！')

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
      message = '给我发邮箱验证码。。。'
      # client.send(message)
      # 反馈信息
      flag = 1
      if flag:
        messagebox.showinfo('验证码已经发送。。。')
      else:
        messagebox.showerror('验证码发送失败。。。')
    Button(login_window, text="获取验证码", font=("Arial", 14),command=get_email_verification_code).pack()

    def login_by_email():
      loginemail = LoginEmail()
      #message = loginemail.get_message(email.get(), email_code.get())
      message = loginemail.get_message(email.get(), email_code.get())
      client.send(message.encode())
      print(message)
      flag = 1
      if flag:
        # 登陆成功，进入个人主页
        messagebox.showinfo('邮箱登陆成功！')
        PersonalInfoWindow(username)
      else:
        messagebox.showinfo('邮箱登陆失败！')

    Button(login_window, text="登录", font=("Arial", 14), command=login_by_email).pack()


def register():
  register_window = Toplevel(window)
  register_window.title("注册")
  register_window.geometry("400x400")

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
    client.send(message.encode())
    print(message)
    # 表示服务器关于注册返回的信息
    flag = 1
    if flag:
      messagebox.showinfo("注册成功")
      PersonalInfoWindow(username)
    else:
      messagebox.showerror("注册失败", "用户名已被占用，请尝试其他用户名！")

  # 创建注册按钮，并在点击时调用register_user方法
  Button(register_window, text="注册", font=("Arial", 14), command=register_user).pack()

def forgot_password():
  forgot_password_window = Toplevel(window)
  forgot_password_window.title("忘记密码")
  forgot_password_window.geometry("400x400")

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
    message = '给我发手机验证码。。。'
    # client.send(message)
    # 反馈信息
    flag = 1
    if flag:
      messagebox.showinfo('验证码已经发送。。。')
    else:
      messagebox.showerror('验证码发送失败。。。')
  Button(forgot_password_window, text="获取验证码", font=("Arial", 14),command=get_phone_verification_code).pack()

  Label(forgot_password_window, text="新密码：", font=("Arial", 14)).pack()
  Entry(forgot_password_window, show="*", font=("Arial", 14),textvariable=new_password1).pack()

  Label(forgot_password_window, text="确认密码：", font=("Arial", 14)).pack()
  Entry(forgot_password_window, show="*", font=("Arial", 14),textvariable=new_password2).pack()

  def forget_password():
    forgetpassword = ForgetPassword()
    message = forgetpassword.get_message(phone_number.get(),phone_code.get(),new_password1.get(),new_password2.get())
    client.send(message.encode())
    print(message)
    # 服务器反馈的关于修改密码的信息
    flag = ''
    if flag:
      messagebox.showinfo('修改密码成功！')
    else:
      messagebox.showinfo('密码修改失败')
  Button(forgot_password_window, text="确认修改", font=("Arial", 14),command=forget_password).pack()


# 创建窗口
window = Tk()
window.title("登录注册系统")
# 设置窗口大小和位置
window.geometry("400x400")
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
