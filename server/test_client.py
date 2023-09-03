#encoding=utf-8

import socket
import os

import tkinter as tk
from tkinter import filedialog

client = socket.socket()  # 生成socket连接对象
ip_port = ('127.0.0.1', 9000)  # 地址和端口号
try:
    client.connect(ip_port)  # 连接
    print('服务器已连接')
except :
    print('服务器连接失败，请修改后重新运行!!')
    exit(0)

while True:
    #content = input(">>")
    content = input('请输入测试的消息:')

    if content=='exit':     #退出操作
        exit(1)

    client.send(content.encode())

    if len(content) == 0:   # 如果传入空字符继续运行
        continue

    if content.startswith("get"):       #下载任务
        client.send(content.encode("utf-8"))  # 传送和接收都是bytes类型

        # 1.先接收长度，如果接收长度报错，说明文件不存在
        server_response = client.recv(1024)
        try:
            file_size = int(server_response.decode("utf-8"))
        except:
            print('文件不存在')
            continue
        print('接收到的大小：', file_size)

        # 2.接收文件内容
        filename = 'new' + content.split(' ')[1]
        f = open(filename, 'wb')
        received_size = 0

        while received_size < file_size:
            size = 0  # 准确接收数据大小，解决粘包
            if file_size - received_size > 1024:  # 多次接收
                size = 1024
            else:  # 最后一次接收完毕
                size = file_size - received_size

            data = client.recv(size)  # 多次接收内容，接收大数据
            data_len = len(data)
            received_size += data_len
            print('已接收：', int(received_size / file_size * 100), "%")
            f.write(data)
        f.close()

    elif content.startswith('put'):          #上传任务
        op, filename = content.split(" ")

        if os.path.isfile(filename):  # 判断文件存在
            # 1.先发送文件大小，让客户端准备接收
            size = os.stat(filename).st_size  # 获取文件大小
            client.send(str(size).encode("utf-8"))  # 发送数据长度
            print('发送的大小：', size)
            # 2.发送文件内容
            f = open(filename, 'rb')
            for line in f:
                client.send(line)  # 发送数据
            f.close()
        else:  # 文件不存在情况
            print('文件不存在')  # 发送数据长度
        f.close()

    else:
        pass
client.close()
