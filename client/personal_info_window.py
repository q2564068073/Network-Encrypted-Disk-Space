import urllib
from tkinter import *
from tkinter import messagebox, simpledialog
from tkinter import filedialog
import os
class PersonalInfoWindow:
  def __init__(self, username,client):

    # 初始化用户名和套接字
    self.username = username
    client = client
    self.window = Tk()
    self.window.title("个人云端存储主页")

    # 获取屏幕的宽度和高度
    screen_width = self.window.winfo_screenwidth()
    screen_height = self.window.winfo_screenheight()
    # 设置窗口的大小为屏幕的大小
    self.window.geometry(f"{screen_width}x{screen_height}")

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

    # 创建刷新菜单
    self.refresh_menu = Menu(self.menu_bar, tearoff=0, font=("Arial", 14))
    self.menu_bar.add_cascade(label="刷新", menu=self.refresh_menu)
    self.refresh_menu.add_command(label="刷新内容", command=self.refresh_window)
    # 添加退出菜单选项
    self.menu_bar.add_command(label="退出", command=self.window.quit)

    # 创建内容区域的Frame
    self.content_frame = Frame(self.window, bg="white")
    self.content_frame.pack(fill=BOTH, expand=True)

    # 初始化内容为个人信息
    self.show_personal_info()

    # 设置窗口样式
    self.window.config(bg="#f9f9f9")
    self.window.option_add("*Font", "Arial 12")

  def show_personal_info(self):
    self.clear_content_frame()
    self.content_frame.config(bg="white")

    info_label = Label(self.content_frame, text="个人信息", font=("Arial", 16), bg="white")
    info_label.pack()

    name_label = Label(self.content_frame, text="姓名：张三", font=("Arial", 12), bg="red")
    name_label.pack()

    age_label = Label(self.content_frame, text="年龄：25", font=("Arial", 12), bg="white")
    age_label.pack()

    phone_label = Label(self.content_frame, text="电话号码：1234567890", font=("Arial", 12), bg="white")
    phone_label.pack()

    edit_button = Button(self.content_frame, text="编辑个人信息", font=("Arial", 12), command=self.edit_personal_info)
    edit_button.pack()

  def show_file_storage(self):
    # 在内容区域显示文件存储
    self.clear_content_frame()
    self.content_frame.config(bg="lightpink")

    # 添加文件列表标题
    file_list_label = Label(self.content_frame, text="文件列表", font=("Arial", 14))
    file_list_label.pack(pady=10)

    # 创建滚动条
    scrollbar = Scrollbar(self.content_frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    # 创建文件列表
    self.file_list = Listbox(self.content_frame, font=("Arial", 12), width=90, height=20, yscrollcommand=scrollbar.set)
    self.file_list.pack()

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
      self.file_list.insert(END, file)

    # 设置文件列表的字体大小
    self.file_list.configure(font=("Arial", 14))

    # 添加上传文件按钮
    upload_button = Button(self.content_frame, text="上传文件", font=("Arial", 12), command=self.upload_file)
    upload_button.pack(pady=10)

    # 添加下载文件按钮
    download_button = Button(self.content_frame, text="下载文件", font=("Arial", 12), command=self.download_file)
    download_button.pack(pady=10)

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

      print(filename,absolute_path)
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
        messagebox.showinfo("上传文件", "文件上传成功！")
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

