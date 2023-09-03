from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

class PersonalInfoWindow:
  def __init__(self, username):
    self.window = Tk()
    self.window.title("个人主页")
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
    # 在内容区域显示个人信息
    self.clear_content_frame()
    self.content_frame.config(bg="white")
    # 添加显示个人信息的代码

  def show_file_storage(self):
    # 在内容区域显示文件存储
    self.clear_content_frame()
    self.content_frame.config(bg="lightgray")
    # 添加显示文件存储的代码

    # 添加文件列表
    file_list_label = Label(self.content_frame, text="文件列表", font=("Arial", 14))
    file_list_label.pack(pady=10)
    self.file_list = Listbox(self.content_frame, font=("Arial", 12), width=60, height=20)
    self.file_list.pack()

    # 添加上传文件按钮
    upload_button = Button(self.content_frame, text="上传文件", font=("Arial", 12), command=self.upload_file)
    upload_button.pack(pady=10)
    # 添加下载文件按钮
    download_button = Button(self.content_frame, text="下载文件", font=("Arial", 12), command=self.download_file)
    download_button.pack(pady=10)

  def upload_file(self):
    # 打开文件选择对话框
    filepath = filedialog.askopenfilename()
    if filepath:
      # 处理文件上传逻辑
      #
      filename = filepath.split("/")[-1]  # 获取文件名
      self.file_list.insert(END, filename)
      messagebox.showinfo("上传文件", "文件上传成功！")

  def download_file(self):
    # 获取选中的文件名
    selected_file = self.file_list.get(self.file_list.curselection())
    if selected_file:
      # 处理文件下载逻辑
      #
      messagebox.showinfo("下载文件", "文件下载成功！")

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

  def clear_content_frame(self):
    # 清空内容区域
    for widget in self.content_frame.winfo_children():
      widget.destroy()

