import shutil
import urllib
from tkinter import *
from tkinter import messagebox, simpledialog
from tkinter import filedialog
import os
from protocol.encryption_utils import *
from protocol.communication import *
from get_message import *




class PersonalInfoWindow:
  def __init__(self, username, client):
    self.client = client
    self.username = username
    self.group_name = ' '
    self.group_key = ' '
    self.window = Tk()
    self.window.title("个人主页")

    # 获取屏幕的宽度和高度
    screen_width = self.window.winfo_screenwidth()
    screen_height = self.window.winfo_screenheight()
    # 设置窗口的大小为屏幕的大小
    self.window.geometry(f"{screen_width - 400}x{screen_height}+400+0")

    # 创建菜单栏
    self.menu_bar = Menu(self.window, font=("Arial", 14))
    self.window.config(menu=self.menu_bar)
    # 创建个人信息菜单
    self.personal_info_menu = Menu(self.menu_bar, tearoff=0, font=("Arial", 14))
    self.menu_bar.add_cascade(label="个人信息", menu=self.personal_info_menu)
    self.personal_info_menu.add_command(label="显示个人信息", command=self.show_personal_info)
    # 创建文件存储菜单
    self.file_storage_menu = Menu(self.menu_bar, tearoff=0, font=("Arial", 14))
    self.menu_bar.add_cascade(label="文件存储", menu=self.file_storage_menu)
    self.file_storage_menu.add_command(label="显示文件存储", command=self.show_file_storage)
    self.file_storage_menu.add_command(label="上传文件", command=self.upload_file)
    self.file_storage_menu.add_command(label="下载文件", command=self.download_file)
    # 创建共享文件菜单
    self.shared_files_menu = Menu(self.menu_bar, tearoff=0, font=("Arial", 14))
    self.menu_bar.add_cascade(label="共享文件", menu=self.shared_files_menu)
    self.shared_files_menu.add_command(label="创建共享群组", command=self.create_group)
    self.shared_files_menu.add_command(label="登入共享群组", command=self.login_group)

    # 添加退出菜单选项
    self.menu_bar.add_command(label="退出", command=self.window.quit)

    # 创建内容区域的Frame
    self.content_frame = Frame(self.window, borderwidth=2, relief="solid")
    self.content_frame.pack(fill=BOTH, expand=True)

    # 初始化内容为个人信息
    self.show_personal_info()

    # 设置窗口样式
    self.window.config(bg="#f9f9f9")
    self.window.option_add("*Font", "Arial 12")

  def show_personal_info(self):
    self.clear_content_frame()
    self.content_frame.config(bg="lightblue")
    # 显示个人姓名
    name_label = Label(self.content_frame, text="用户姓名：", font=("Arial", 16, "bold"), bg="lightblue")
    name_label.grid(row=0, column=0, padx=20, pady=20, sticky="e")
    # 显示个人姓名的值
    print(self.username)
    name_value = Label(self.content_frame, text=self.username, font=("Arial", 16), bg="lightblue")
    name_value.grid(row=0, column=1, padx=20, pady=20, sticky="w")
    # 显示分割线
    separator = Frame(self.content_frame, height=2, bd=1, relief="sunken")
    separator.grid(row=1, columnspan=2, sticky="we", padx=20, pady=10)
    # 显示关于软件的功能说明和关于信息
    info_label = Label(self.content_frame, text="关于软件", font=("Arial", 14, "bold"), bg="lightblue")
    info_label.grid(row=2, column=0, columnspan=2, padx=20, pady=20)
    function_label = Label(self.content_frame, text="功能说明：\n1. 提供网络共享存储空间：系统需要提供一个网络共享存储空间，供用户存储和共享文件。"
                                                    "\n2. 用户存储加密空间：每个用户有自己的存储加密空间，确保用户之间的数据隔离和安全性。"
                                                    "\n3. 数据和文件的加密传输：系统需要支持数据和文件的加密传输，保护数据在传输过程中的安全性。"
                                                    "\n4. 本地加密存储：共享存储空间的数据需要进行本地加密存储，确保数据在存储过程中的安全性。"
                                                    "\n5. 一次一密加密传输机制：文件加密传输支持一次一密加密传输机制，提高数据传输的安全性。"
                                                    "\n6. 防篡改和防中间人攻击：系统需要支持防篡改和防中间人攻击，保护数据传输过程中的完整性和安全性。"
                                                    "\n7. 安全的加密数据找回机制：系统需要提供安全的加密数据找回机制，确保用户可以找回加密的数据。"
                           , font=("Arial", 12), bg="lightblue", justify="left")
    function_label.grid(row=3, column=0, columnspan=2, padx=20, pady=10)
    # 显示分割线
    separator = Frame(self.content_frame, height=2, bd=1, relief="sunken")
    separator.grid(row=4, columnspan=2, sticky="we", padx=20, pady=10)
    # 显示关于信息
    about_label = Label(self.content_frame, text="介绍：系统需是基于网络编程技术，为互联网、无线网络和移动通信等用户提供一个安全的网络存储空间。", font=("Arial", 12),
                        bg="lightblue")
    about_label.grid(row=5, column=0, columnspan=2, padx=20, pady=10)
    # 设置内容框架的列权重，使信息居中显示
    self.content_frame.columnconfigure(0, weight=1)
    self.content_frame.columnconfigure(1, weight=1)

  def show_file_storage(self):
    # 在内容区域显示文件存储
    self.clear_content_frame()
    self.content_frame.config(bg="lightblue")

    # 添加文件列表标题
    file_list_label = Label(self.content_frame, text="个人文件列表", font=("Arial", 14))
    file_list_label.pack(pady=10)

    # 创建滚动条
    scrollbar = Scrollbar(self.content_frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    # 创建文件列表
    self.file_list = Listbox(self.content_frame, font=("Arial", 12), width=90, height=10, yscrollcommand=scrollbar.set)
    self.file_list.pack()

    # 设置滚动条与文件列表的关联
    scrollbar.config(command=self.file_list.yview)

    # 假设文件列表为一个字符串列表
    '''
    这里有问题，就是用户的文件列表名的列表怎样从后端即时传进来
    '''
    # files = ["file1.txt", "file2.txt", "file3.txt", "file4.txt", "file5.txt", "file6.txt",
    #          "file7.txt", "file8.txt", "file9.txt", "file10.txt", "file11.txt", "file12.txt",
    #          "file13.txt", "file14.txt", "file15.txt", "file16.txt", "file17.txt", "file18.txt",
    #          "file19.txt", "file20.txt", "file21.txt", "file22.txt", "file23.txt", "file24.txt",
    #          "file25.txt", "file26.txt", "file27.txt", "file28.txt", "file29.txt", "file30.txt"]
    files = []
    upload = Upload()
    message_send = upload.get_list_message(self.username)
    send_message(self.client,message_send)
    message_return = receive_message(self.client)
    print("文件列表")
    print(message_return)
    if message_return == '没有文件':
      files = []
    else:
      files = message_return
    
    #for file in files:
    #print(type(files))
    files=eval(files)
    #print(type(files))
    for file in files:
      self.file_list.insert(END, file)
    #file_list = files

    # 设置文件列表的字体大小
    self.file_list.configure(font=("Arial", 14))

    # 添加上传文件按钮
    upload_button = Button(self.content_frame, text="上传文件", font=("Arial", 12), command=self.upload_file,
                           bg='lightblue', fg='white')
    upload_button.pack(pady=10)
    # 添加下载文件按钮
    download_button = Button(self.content_frame, text="下载文件", font=("Arial", 12), command=self.download_file,
                             bg='lightblue', fg='white')
    download_button.pack(pady=10)
    # 添加刷新按钮
    refresh_button = Button(self.content_frame, text="刷新", font=("Arial", 12), command=self.refresh_file,
                            bg='lightblue', fg='white')
    refresh_button.pack(pady=10)

  def upload_shared_file(self):
    print("群密钥："+self.group_key)
    print("群名："+self.group_name)

    filepath = filedialog.askopenfilename()
    if filepath:
      # 获取文件名
      filename = os.path.basename(filepath)
      print("文件名：" + filename)
      # 获取文件的绝对路径
      absolute_path = os.path.abspath(filepath)
      print("文件路径：" + absolute_path)
      group = Group()
      data, key_hash = rc4_file(absolute_path, self.group_key)
      message = group.upload_group(self.group_name, filename)
      print(message)
      send_message(self.client, message)
      message_response = receive_message(self.client)
      if message_response == 'ok':
        print(message_response)
        self.client.send_encrypt(data)
        messagebox.showinfo("上传文件", "文件上传成功！")
      elif message_response == '0':
        messagebox.showerror("上传错误", "文件已重复上传")
        
  def download_shared_file(self):
    # 获取选中的文件名
    selected_file = self.shared_files_list.get(self.shared_files_list.curselection())
    print(selected_file)
    # 如果有选中文件
    if selected_file:
      # 文件下载URL
      '''
      这里的下载文件路径还有问题，暂时用这个代替，按理来说是一个用户点击了一个文件名，选择了下载，客户端应该
      将下载信息传给后端，在返回。
      '''
      group = Group()
      #key_hash = get_hash(self.group_key.encode('utf-8'))
      message = group.download_group(self.group_name, selected_file)
      print(message)
      send_message(self.client, message)
      #message_return = receive_message(self.client)
      #message_return = '2'
      # if message_return == '2':
      #   message_2 = 'ok'
      #   send_message(self.client, message_2)
      data = self.client.recv_decrypt()
      print(data)

      s_box = rc4_key_schedule(self.group_key)
      keystream = generate_rc4_keystream(s_box, len(data))
      text = rc4_en_de_crypt(data, keystream)

      file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("所有文件", "*"),))
      print(file_path)
      # 保存文件
      with open(file_path, "wb") as file:
        file.write(text)
      print("文件保存成功")
      print(text)
      messagebox.showinfo("文件保存成功", f"已保存为{file_path}")
      # elif message_return == '1' or message_return == '0':
      #   messagebox.showerror("密码错误", "请重新下载")
    else:
      messagebox.showwarning("下载文件", "请先选择要下载的文件！")

  def refresh_file(self):
    """
    刷新文件页面
    """
    print(1)
    self.show_file_storage()

  def refresh_shared_file(self):
    """
    刷新共享页面
    """
    print(2)
    self.show_shared_files()

  def upload_file(self):
    """
    上传文件，获取上传文件的绝对路径，名称，以及用户输入的加密文件的密钥。
    :return:
    """
    # 打开文件选择对话框
    filepath = filedialog.askopenfilename()
    if filepath:

      # 获取文件名
      filename = os.path.basename(filepath)
      print("文件名："+ filename)
      # 获取文件的绝对路径
      absolute_path = os.path.abspath(filepath)
      print("文件路径：" + absolute_path)
      # 弹出输入框，让用户输入密钥
      key = simpledialog.askstring("输入密钥", "请输入加密文件的密钥：", show='*')
      confirm_key = simpledialog.askstring("确认密钥", "请再次输入密钥以确认：", show='*')
      #id_number = simpledialog.askstring("身份证校验","请输入身份证后四位",show='*')

      # 检查密钥是否一致
      if key == confirm_key:
        # 处理文件上传逻辑”
        #print(key)
        '''
        这里添加那个文件查找加密的函数，传入参数为absolute_path,key
        '''
        upload = Upload()
        #username
        #print("用户名："+self.username)
        data, key_hash = rc4_file(absolute_path, key)
        message = upload.upload_message(self.username,filename,key_hash)
        send_message(self.client,message)
        message_response = receive_message(self.client)
        if message_response == 'ok':
          self.client.send_encrypt(data)
          messagebox.showinfo("上传文件", "文件上传成功！")
        elif message_response == '0':
          messagebox.showerror("上传错误","文件已重复上传")
      else:
        messagebox.showerror("密钥错误", "密钥输入不一致，请重新上传文件并输入正确的密钥！")

  def download_file(self):
    # 获取选中的文件名
    selected_file = self.file_list.get(self.file_list.curselection())
    print(selected_file)
    # 如果有选中文件
    if selected_file:
      # 文件下载URL
      '''
      这里的下载文件路径还有问题，暂时用这个代替，按理来说是一个用户点击了一个文件名，选择了下载，客户端应该
      将下载信息传给后端，在返回。
      '''
      key = simpledialog.askstring("输入密钥", "请输入加密文件的密钥：", show='*')
      upload = Upload()
      key_hash = get_hash(key.encode('utf-8'))
      message = upload.download_message(self.username,selected_file,key_hash)
      send_message(self.client,message)
      message_return = receive_message(self.client)
      if message_return == '2':
        message_2 = 'ok'
        send_message(self.client,message_2)
        data = self.client.recv_decrypt()
        print(data)
        
        s_box=rc4_key_schedule(key)
        keystream=generate_rc4_keystream(s_box,len(data))
        text=rc4_en_de_crypt(data,keystream)
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("所有文件", "*"),))
        print(file_path)
        # 保存文件
        with open(file_path, "wb") as file:
            file.write(text)
        print("文件保存成功")
        print(text)
        messagebox.showinfo("文件保存成功",f"已保存为{file_path}")
      elif message_return == '1' or message_return == '0':
        messagebox.showerror("密码错误","请重新下载")
    else:
      messagebox.showwarning("下载文件", "请先选择要下载的文件！")


  def show_shared_files(self):
    # 在内容区域显示共享文件
    self.clear_content_frame()
    self.content_frame.config(bg="lightgray")
    # 添加显示共享文件的代码
    shared_files_label = Label(self.content_frame, text="共享文件列表", font=("Arial", 14))
    shared_files_label.pack(pady=10)
    self.shared_files_list = Listbox(self.content_frame, font=("Arial", 12), width=90, height=10)
    self.shared_files_list.pack()
    # # 添加下载共享文件按钮
    # download_shared_button = Button(self.content_frame, text="下载共享文件", font=("Arial", 12), command=self.download_shared_file)
    # download_shared_button.pack(pady=10)

    files = []
    group = Group()
    message_send = group.get_group_list(self.group_name)
    send_message(self.client, message_send)
    message_return = receive_message(self.client)
    print("文件列表")
    print(message_return)
    if message_return == '没有文件':
      files = []
    else:
      files = message_return
    files = eval(files)
    #files = ['1.txt','2.txt','3.txt']
    print(type(files))
    for file in files:
      self.shared_files_list.insert(END, file)
    #file_list = files

    #设置文件列表的字体大小
    self.shared_files_list.configure(font=("Arial", 14))

    # 添加上传文件按钮
    upload_button = Button(self.content_frame, text="上传文件", font=("Arial", 12), command=self.upload_shared_file,
                           bg='lightblue', fg='white')
    upload_button.pack(pady=10)
    # 添加下载文件按钮
    download_button = Button(self.content_frame, text="下载文件", font=("Arial", 12), command=self.download_shared_file,
                             bg='lightblue', fg='white')
    download_button.pack(pady=10)
    # 添加刷新按钮
    refresh_button = Button(self.content_frame, text="刷新", font=("Arial", 12), command=self.refresh_shared_file,
                            bg='lightblue', fg='white')
    refresh_button.pack(pady=10)

  def create_group(self):
    """
    创建群聊
    :return:
    """
    group_name = simpledialog.askstring("共享群名", "请输入共享群名")
    group_key = simpledialog.askstring("群密钥", "请输入群密钥")
    print(group_key, group_name)
    self.creat_group_button(group_name,group_key)

  def login_group(self):
    """
    进入群聊
    :return:
    """
    group_name = simpledialog.askstring("共享群名", "请输入共享群名")
    group_key = simpledialog.askstring("群密钥", "请输入群密钥")

    #将群名和群密钥存在对象的属性中
    self.group_name = group_name
    self.group_key = group_key

    print(group_key, group_name)

    self.login_group_button(group_name, group_key)

    self.show_shared_files()

  def creat_group_button(self, group_name, group_key):
    group = Group()
    group_key = get_hash(group_key.encode())
    print(group_key)
    message = group.create_group(group_name, group_key)
    # print(message)
    send_message(self.client, message)
    flag = receive_message(self.client)
    print(flag)  # 注册的结果应该有对应的框，此处好像没有看到
    if flag == '0':
      messagebox.showerror("创建失败", "群名已存在！")
    elif flag == '1':
      messagebox.showinfo("创建成功", "群创建成功！")

  # 跳转使用界面
  # 创建注册按钮，并在点击时调用register_user方法

  def login_group_button(self, group_name, group_key):
    group = Group()
    group_key = get_hash(group_key.encode())
    message = group.login_group(group_name, group_key)
    send_message(self.client, message)
    print(message)
    flag = receive_message(self.client)
    # print(flag)
    if flag == '0':  # 群名不存在
      messagebox.showerror("登录失败", "群名不存在！")
    elif flag == '1':  # 密码错误
      messagebox.showerror("登录失败", "群密码错误！")
    elif flag == '2':  # 登录成功
      messagebox.showinfo("登录成功", "登录成功！")


    # 调用刷新共享空间方法


  # def upload_shared_file(self):
  #   """
  #       向群组上传文件，获取上传文件的绝对路径，名称
  #       :return:
  #       """
  #   # 打开文件选择对话框
  #   filepath = filedialog.askopenfilename()
  #   if filepath:
  #
  #     # 获取文件名
  #     filename = os.path.basename(filepath)
  #     print("文件名：" + filename)
  #     # 获取文件的绝对路径
  #     absolute_path = os.path.abspath(filepath)
  #     print("文件路径：" + absolute_path)
  #     # 弹出输入框，让用户输入密钥
  #     key = simpledialog.askstring("输入密钥", "请输入加密文件的密钥：", show='*')
  #     confirm_key = simpledialog.askstring("确认密钥", "请再次输入密钥以确认：", show='*')
  #     # id_number = simpledialog.askstring("身份证校验","请输入身份证后四位",show='*')
  #
  #     # 检查密钥是否一致
  #     if key == confirm_key:
  #       # 处理文件上传逻辑”
  #       # print(key)
  #       '''
  #       这里添加那个文件查找加密的函数，传入参数为absolute_path,key
  #       '''
  #       upload = Upload()
  #       # username
  #       # print("用户名："+self.username)
  #       data, key_hash = rc4_file(absolute_path, key)
  #       message = upload.upload_message(self.username, filename, key_hash)
  #       send_message(self.client, message)
  #       message_response = receive_message(self.client)
  #       if message_response == 'ok':
  #         self.client.send_encrypt(data)
  #         messagebox.showinfo("上传文件", "文件上传成功！")
  #       elif message_response == '0':
  #         messagebox.showerror("上传错误", "文件已重复上传")
  #     else:
  #       messagebox.showerror("密钥错误", "密钥输入不一致，请重新上传文件并输入正确的密钥！")
  #
  # def download_shared_file(self):
  #   # 获取选中的共享文件名
  #   selected_shared_file = self.shared_files_list.get(self.shared_files_list.curselection())
  #   if selected_shared_file:
  #     # 处理共享文件下载逻辑
  #     #
  #     messagebox.showinfo("下载共享文件", "共享文件下载成功！")

  def clear_content_frame(self):
    # 清空内容区域
    for widget in self.content_frame.winfo_children():
      widget.destroy()

#发送消息
def send_message(safe_socket,message):
  safe_socket.send_encrypt(message.encode())

#接收消息，返回接收到的字符串
def receive_message(safe_socket):
  response = safe_socket.recv_decrypt().decode('utf-8', errors='ignore')
  return response