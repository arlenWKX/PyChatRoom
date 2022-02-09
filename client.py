import tkinter
from tkinter import messagebox
import json,time
import threading
import select
from socket import *
import os

SERVER_HOST = gethostname()
SERVER_PORT = 1200
    

def client_draw_draw_login(self): #登录页面
    print ( '[ ] Drawing login interface', end='' )
    self.root.title("聊天室登录页面")  # 给主窗口设置标题内容
    self.root.geometry('450x300') # 设置主窗口大小
    self.canvas = tkinter.Canvas(self.root, height=200, width=500)  # 创建画布
    self.label_account = tkinter.Label(self.root, text='账 号')  # 创建一个`Label`名为`账 号: `
    self.label_password = tkinter.Label(self.root, text='密 码')  # 创建一个`Label`名为`密 码: `
    self.input_account = tkinter.Entry(self.root, width=30)  # 创建一个账号输入框,并设置尺寸
    self.input_password = tkinter.Entry(self.root, show='*', width=30)  # 创建一个密码输入框,并设置尺寸
    self.login_button = tkinter.Button(self.root, command=self.verify_login, text="登 录", width=10) #登录按钮
    self.register_button = tkinter.Button(self.root, command=self.register_interface, text="注 册", width=10) #注册按钮

    # 登录页面各个控件进行布局
    self.label_account.place(x=90, y=70)
    self.label_password.place(x=90, y=150)
    self.input_account.place(x=135, y=70)
    self.input_password.place(x=135, y=150)
    self.login_button.place(x=120, y=235)
    self.register_button.place(x=250, y=235)
    print ( '\r[+] Drawing login interface' )


def client_draw_draw_register(self): #注册页面控件创
    print ( '[ ] Drawing register interface', end='' )
    self.login_button.destroy()
    self.register_button.destroy()
    self.root.title("聊天室注册页面")
    self.root.geometry('450x300') # 设置主窗口大小
    self.canvas = tkinter.Canvas(self.root, height=200, width=500)  # 创建画布
    self.label_nickname = tkinter.Label(self.root, text='昵 称')  # 创建一个"Label",名为："昵 称"
    self.input_nickname = tkinter.Entry(self.root, width=30)  # 创建一个昵称输入框,并设置尺寸
    self.register_submit_button = tkinter.Button(self.root, command=self.verify_register, text="提交注册", width=10) #创建注册按钮
    self.return_login_button = tkinter.Button(self.root, command=self.return_login_interface, text="返回登录",width=10)  # 创建注册按钮

    # 注册页面各个控件进行布局
    self.label_account.place(x=90, y=70)
    self.label_password.place(x=90, y=130)
    self.input_account.place(x=135, y=70)
    self.input_password.place(x=135, y=130)
    self.label_nickname.place(x=90, y=190)
    self.input_nickname.place(x=135, y=190)
    self.register_submit_button.place(x=120, y=235)
    self.return_login_button.place(x=250, y=235)
    print ( '\r[+] Drawing register interface' )


def client_draw_draw_chat(self,nickname):
    print ( '[ ] Drawing chat interface', end='' )
    self.root.title("【%s】的聊天室页面" %nickname)  # 给主窗口设置标题内容
    self.root.geometry('520x560')
    # 创建frame容器
    self.frmLT = tkinter.Frame(width=500, height=320)
    self.frmLC = tkinter.Frame(width=500, height=150)
    self.frmLB = tkinter.Frame(width=500, height=30)

    self.txtMsgList = tkinter.Text(self.frmLT)
    self.txtMsgList.tag_config('DimGray', foreground='#696969',font=("Times", "11"))  #设置消息时间字体样式
    self.txtMsgList.tag_config('Blue4', foreground='#00008B', font=("Message", "13"),spacing2=5) #设置自己的消息字体样式
    self.txtMsgList.tag_config('Black', foreground='#000000', font=("Message", "13"), spacing2=5)  # 设置其它人的消息字体样式

    self.txtMsg = tkinter.Text(self.frmLC)
    self.txtMsg.bind("<Control-Return>", self.sendMsgEvent) # 触发键盘的回车按键事件，发送消息
    self.btnSend = tkinter.Button(self.frmLB, text='发送', width=12, command=self.sendMsg)
    self.labSend = tkinter.Label(self.frmLB, width=55) #创建空的Label在左边占个位置，便于发送按钮靠右

    # 窗口布局
    self.frmLT.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    self.frmLC.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    self.frmLB.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # 固定大小
    self.frmLT.grid_propagate(0)
    self.frmLC.grid_propagate(0)
    self.frmLB.grid_propagate(0)

    self.labSend.grid(row=0, column=0)
    self.btnSend.grid(row=0, column=1)  #发送按钮布局
    self.txtMsgList.grid()
    self.txtMsg.grid()

    # WM_DELETE_WINDOW 不能改变，这是捕获命令
    self.root.protocol('WM_DELETE_WINDOW', self.on_closing)
    print ( '\r[+] Drawing chat interface' )

class ChatRoom(object):
    def connect(self): #配置连接
        print ( '[ ] Connecting to server', end='' )
        self.s = socket(AF_INET, SOCK_STREAM)
        remote_host = SERVER_HOST #获取计算机名称
        port = SERVER_PORT  #设置端口号
        self.s.connect((remote_host, port))  # 发起连接
        print ( '\r[+] Successfully connected from %s to %s'%(self.s.getsockname(),self.s.getpeername()) )
        return self.s

    def recive(self,s): # 监听消息
        self.my = [s]
        while True:
         rs, ws, es = select.select(self.my, [], [])
         if s in rs:
             try:
                 data = s.recv(1024)
                 data_dict=json.loads(data.decode('utf-8'))
                 type = data_dict["type"] # 根据服务端返回的type值，进入不同逻辑
                 if type == "login": # 登录逻辑
                     if "000000" == data_dict["code"]: #code返回000000，跳转聊天页面
                         nickname = data_dict["nickname"]
                         self.chat_interface(nickname)
                     else:
                         tkinter.messagebox.showinfo(title='登录提示', message=data_dict["msg"])
                 elif type == "register": # 注册逻辑
                     if "000000" == data_dict["code"]:  #code返回000000，跳转聊天页面
                         nickname = data_dict["nickname"]
                         tkinter.messagebox.showinfo(title='进入聊天室', message=data_dict["msg"])
                         self.chat_interface(nickname)
                     else:
                         tkinter.messagebox.showinfo(title='注册提示', message=data_dict["msg"])
                 elif type == "chat": # 聊天逻辑
                     message = data_dict["message"]
                     nickname = data_dict["nickname"]
                     isMy = data_dict["isMy"]
                     times = " "+ nickname + "\t" + time.strftime("%H:%M:%S",time.localtime())+ '\n'
                     self.txtMsgList.insert(tkinter.END, times,"DimGray") # 聊天页面，发送人以及发送时间展示
                     if "yes" == isMy: # 如果是自己发的消息，字体使用'DarkTurquoise'，如果是别人发的消息，字体使用'Black'
                        self.txtMsgList.insert(tkinter.END,  " "+ message + "\n\n",'DarkTurquoise')
                     else:
                         self.txtMsgList.insert(tkinter.END, " " + message + "\n\n", 'Black')
                     self.txtMsgList.see(tkinter.END) # 插入消息时，自动滚动到底部

             except Exception as e:
                 print(e)
                 exit()


    def register_interface(self): # 进入注册界面
        client_draw_draw_register(self)

    def chat_interface(self,nickname): #进入聊天页面
        client_draw_draw_chat(self,nickname)

    def return_login_interface(self): #返回登录页面
        self.label_nickname.destroy() #将不需要的label_nickname控件先销毁
        self.input_nickname.destroy() #将不需要的input_nickname控件先销毁
        self.label_password.destroy() #将不需要的label_password控件先销毁
        self.input_password.destroy() #将不需要的input_password控件先销毁
        client_draw_draw_login(self)


    def verify_register(self): # 获取输入框内容，进行注册验证
        print ( '[ ] Verifying register', end='' )
        account = self.input_account.get()
        password = self.input_password.get()
        nickname = self.input_nickname.get()
        try:
            register_data = {}
            register_data["type"] = "register"
            register_data["account"] = account
            register_data["password"] = password
            register_data["nickname"] = nickname
            data = json.dumps(register_data) #将register_data由dict格式转为json字符串，便于网络传输
            self.s.send(data.encode('utf-8'))
        except Exception as e:
            print(e)
            return
        print ( '\r[+] Verifying register... Done' )

    def verify_login(self): # 获取输入框内容，进行登录信息验证
        print ( '[ ] Verifying login', end='' )
        account = self.input_account.get()
        password = self.input_password.get()
        try:
            login_data = {}
            login_data["type"] = "login"
            login_data["account"] = account
            login_data["password"] = password
            data = json.dumps(login_data)  #将login_data由dict格式转为json字符串，便于网络传输
            self.s.send(data.encode('utf-8'))
        except Exception as e:
            print(e)
        print ( '\r[+] Verifying login... Done' )


    def sendMsg(self):#获取输入框内容，发送消息
        message = self.txtMsg.get('0.0', tkinter.END).strip()
        if not message:
            tkinter.messagebox.showinfo(title='发送提示', message="发送内容不能为空，请重新输入")
            return
        self.txtMsg.delete('0.0', tkinter.END)
        try:
            chat_data = {}
            chat_data["type"] = "chat"
            chat_data["message"] = message
            data = json.dumps(chat_data) #将chat_data由dict格式转为json字符串，便于网络传输
            self.s.send(data.encode('utf-8'))
            
        except Exception as e:
            print(e)

    def sendMsgEvent(self,event):#发送消息事件
        if event.keysym =='Return': #如果捕捉到键盘的回车按键，触发消息发送
            self.sendMsg()

    def on_closing(self):  # 聊天页面，点击右上角退出时执行
        if messagebox.askokcancel("退出提示", "是否离开聊天室？"):
            self.root.destroy()
            os.exit(0)

def main():
    chatRoom = ChatRoom()
    client = chatRoom.connect()
    t = threading.Thread(target=chatRoom.recive, args=(client,)) # 创建一个线程，监听消息
    t.start()
    chatRoom.root = tkinter.Tk()  # 创建主窗口,用于容纳其它组件
    client_draw_draw_login(chatRoom) # 登录界面控件创建、布局
    tkinter.mainloop() # 进入事件（消息）循环


if __name__ == '__main__':
    main()

