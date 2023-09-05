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
    self.shared_files_menu.add_command(label="查看共享文件", command=self.show_shared_files)
    self.shared_files_menu.add_command(label="上传共享文件", command=self.upload_shared_file)
    self.shared_files_menu.add_command(label="下载共享文件", command=self.download_shared_file)

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

    # 向后端发送查询个人信息的请求
    # self.client.send("get_personal_info")
    # self.client.send(self.username)
    # 接收后端返回的个人信息
    # personal_info = self.client.receive()
    #global name
    personal_info = {'name': 'name', 'age': 25, 'phone': '1234567890'}
    # 创建表格来展示个人信息
    table_frame = Frame(self.content_frame, bg="white")
    table_frame.pack(pady=20)

    # 创建表格的标题行
    name_label = Label(table_frame, text="姓名", font=("Arial", 12, "bold"), bg="white")
    name_label.grid(row=0, column=0, padx=10, pady=5)
    age_label = Label(table_frame, text="年龄", font=("Arial", 12, "bold"), bg="white")
    age_label.grid(row=0, column=1, padx=10, pady=5)
    phone_label = Label(table_frame, text="电话号码", font=("Arial", 12, "bold"), bg="white")
    phone_label.grid(row=0, column=2, padx=10, pady=5)

    # 创建表格的数据行
    name_value = Label(table_frame, text=personal_info["name"], font=("Arial", 12), bg="white")
    name_value.grid(row=1, column=0, padx=10, pady=5)
    age_value = Label(table_frame, text=personal_info["age"], font=("Arial", 12), bg="white")
    age_value.grid(row=1, column=1, padx=10, pady=5)
    phone_value = Label(table_frame, text=personal_info["phone"], font=("Arial", 12), bg="white")
    phone_value.grid(row=1, column=2, padx=10, pady=5)

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
    
    # for file in files:
    self.file_list.insert(END, files)

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
      # 获取文件的绝对路径
      absolute_path = os.path.abspath(filepath)

      # 目标保存路径
      target_folder = r"C:\Users\熊兵\OneDrive\桌面\files"
      # 构建目标文件的完整路径
      target_path = os.path.join(target_folder, filename)
      # 复制文件到目标路径
      shutil.copyfile(filepath, target_path)

      print(filename, absolute_path)
      # 弹出输入框，让用户输入密钥
      key = simpledialog.askstring("输入密钥", "请输入加密文件的密钥：", show='*')
      confirm_key = simpledialog.askstring("确认密钥", "请再次输入密钥以确认：", show='*')

      # 检查密钥是否一致
      if key == confirm_key:
        # 处理文件上传逻辑
        print(key)
        '''
        这里添加那个文件查找加密的函数，传入参数为absolute_path,key

        '''
        # file_message = 文件加密函数(absolute_path,key)
        # file_message = 'hello'
        # self.client.send(file_message)

        messagebox.showinfo("上传文件", "文件上传成功！")
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
      将下载信息传给后端，在返回文件的具体内容。
      '''
      url = "https://example.com/files/" + selected_file

      # 弹出对话框，让用户选择保存文件的路径和文件名
      file_path = filedialog.asksaveasfilename()

      # 如果用户选择了保存路径
      if file_path:
        try:
          # urllib.request.urlretrieve(url, file_path)
          # 目标保存路径
          target_folder = r"C:\Users\熊兵\OneDrive\桌面\files"
          # 构建目标文件的完整路径
          target_path = os.path.join(target_folder, selected_file)
          # 复制文件到目标路径
          shutil.copyfile(file_path, target_path)

          messagebox.showinfo("下载文件", "文件下载成功！")
        except Exception as e:
          messagebox.showerror("下载文件", "文件下载失败：" + str(e))
      else:
        messagebox.showwarning("下载文件", "未选择保存路径！")
    else:
      messagebox.showwarning("下载文件", "请先选择要下载的文件！")

  def show_shared_files(self):
    # 在内容区域显示共享文件
    self.clear_content_frame()
    self.content_frame.config(bg="lightblue")
    # 添加显示共享文件的代码
    shared_files_label = Label(self.content_frame, text="共享文件列表", font=("Arial", 14))
    shared_files_label.pack(pady=10)

    # 创建滚动条
    scrollbar = Scrollbar(self.content_frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    # 创建文件列表
    self.shared_files_list = Listbox(self.content_frame, font=("Arial", 12), bg="lightgreen", width=90, height=10,
                                     yscrollcommand=scrollbar.set)
    self.shared_files_list.pack()

    # 设置滚动条与文件列表的关联
    scrollbar.config(command=self.file_list.yview)

    # 假设文件列表为一个字符串列表
    '''
    这里有问题，就是用户的文件列表名的列表怎样从后端即时传进来
    '''
    files = ["file1.txt", "file2.txt", "file3.txt", "file4.txt", "file5.txt", "file6.txt",
             "file7.txt", "file8.txt", "file9.txt", "file10.txt", "file11.txt", "file12.txt",
             "file13.txt", "file14.txt", "file15.txt", "file16.txt", "file17.txt", "file18.txt",
             "file19.txt", "file20.txt", "file21.txt", "file22.txt", "file23.txt", "file24.txt",
             "file25.txt", "file26.txt", "file27.txt", "file28.txt", "file29.txt", "file30.txt"]

    for file in files:
      self.shared_files_list.insert(END, file)

    # 设置文件列表的字体大小
    self.shared_files_list.configure(font=("Arial", 14))

    # 添加下载共享文件按钮
    upload_shared_button = Button(self.content_frame, text="上传共享文件", font=("Arial", 12),
                                  command=self.upload_shared_file, bg='lightblue', fg='white')
    upload_shared_button.pack(pady=10)
    # 添加下载共享文件按钮
    download_shared_button = Button(self.content_frame, text="下载共享文件", font=("Arial", 12),
                                    command=self.download_shared_file, bg='lightblue', fg='white')
    download_shared_button.pack(pady=10)
    # 添加刷新按钮
    refresh_button = Button(self.content_frame, text="刷新", font=("Arial", 12), command=self.refresh_shared_file,
                            bg='lightblue', fg='white')
    refresh_button.pack(pady=10)

  def upload_shared_file(self):
    # 打开文件选择对话框
    filepath = filedialog.askopenfilename()
    if filepath:
      # 处理共享文件上传逻辑
      #
      filename = filepath.split("/")[-1]  # 获取文件名
      self.shared_files_list.insert(END, filename)
      messagebox.showinfo("上传共享文件", "共享文件上传成功！")

  def download_shared_file(self):
    # 获取选中的共享文件名
    selected_shared_file = self.shared_files_list.get(self.shared_files_list.curselection())
    if selected_shared_file:
      # 处理共享文件下载逻辑
      #
      messagebox.showinfo("下载共享文件", "共享文件下载成功！")

  def clear_content_frame(self):
    # 清空内容区域
    for widget in self.content_frame.winfo_children():
      widget.destroy()

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

  def get_list(self):
    upload = Upload()
    message = upload.get_list_message(self.Username)
    print(message)
    self.Client.send(message.encode())
    response = self.Client.recv(1024).decode()
    print(response)


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

      # 检查密钥是否一致
      if key == confirm_key:
        # 处理文件上传逻辑
        print(key)
        '''
        这里添加那个文件查找加密的函数，传入参数为absolute_path,key
        '''
        upload = Upload()
        #username
        print("用户名："+self.username)
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

    # 如果有选中文件
    if selected_file:
      # 文件下载URL
      '''
      这里的下载文件路径还有问题，暂时用这个代替，按理来说是一个用户点击了一个文件名，选择了下载，客户端应该
      将下载信息传给后端，在返回。
      '''
      url = "https://example.com/files/" + selected_file

      # 弹出对话框，让用户选择保存文件的路径和文件名
      file_path = filedialog.asksaveasfilename()

      # 如果用户选择了保存路径
      if file_path:
        try:
          urllib.request.urlretrieve(url, file_path)
          messagebox.showinfo("下载文件", "文件下载成功！")
        except Exception as e:
          messagebox.showerror("下载文件", "文件下载失败：" + str(e))
      else:
        messagebox.showwarning("下载文件", "未选择保存路径！")
    else:
      messagebox.showwarning("下载文件", "请先选择要下载的文件！")

  def show_shared_files(self):
    # 在内容区域显示共享文件
    self.clear_content_frame()
    self.content_frame.config(bg="lightgray")
    # 添加显示共享文件的代码
    shared_files_label = Label(self.content_frame, text="共享文件列表", font=("Arial", 14))
    shared_files_label.pack(pady=10)
    self.shared_files_list = Listbox(self.content_frame, font=("Arial", 12), width=60, height=20)
    self.shared_files_list.pack()
    # 添加下载共享文件按钮
    download_shared_button = Button(self.content_frame, text="下载共享文件", font=("Arial", 12), command=self.download_shared_file)
    download_shared_button.pack(pady=10)

  def upload_shared_file(self):
    # 打开文件选择对话框
    filepath = filedialog.askopenfilename()
    if filepath:
      # 处理共享文件上传逻辑
      #
      filename = filepath.split("/")[-1]  # 获取文件名
      self.shared_files_list.insert(END, filename)
      messagebox.showinfo("上传共享文件", "共享文件上传成功！")

  def download_shared_file(self):
    # 获取选中的共享文件名
    selected_shared_file = self.shared_files_list.get(self.shared_files_list.curselection())
    if selected_shared_file:
      # 处理共享文件下载逻辑
      #
      messagebox.showinfo("下载共享文件", "共享文件下载成功！")

  def refresh_window(self,username):
    # 刷新窗口的方法，关闭当前窗口并重新创建一个新的个人主页窗口
    self.window.destroy()
    PersonalInfoWindow(username=username)

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