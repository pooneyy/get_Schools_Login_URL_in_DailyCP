#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-05-05 10:37:41
# @Author  : Qiuyelin
# @File    : getSchoolLoginURL_GUI.py
# @Software: Visual Studio Code

import json
import webbrowser
from tkinter import *
from tkinter.constants import END

import requests


class GUI():
    '''窗口对象'''

    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("查询高校今日校园登录接口")  
        self.init_window_name.geometry('510x612+500+70')
        self.init_window_name.resizable(width=False, height=False) # 禁止改变窗口大小
        # self.init_window_name.iconbitmap('logo.ico')
        
        # 标签
        self.init_data_label = Label(self.init_window_name, text="输入学校名称：",font=("宋体",13))
        self.init_data_label.grid(row=0, column=0)

        # 输入框
        self.init_data_input = Entry(self.init_window_name, width=20,font=("宋体",13))
        self.init_data_input.grid(row=0, column=1)
        # 点击输入框清空输入框
        self.init_data_input.bind('<Button-1>', lambda event: self.init_data_input.delete(0, END))

        # 按钮
        self.init_data_button = Button(self.init_window_name, text="查询",font=("宋体",13), width=10, height=1, command=lambda: GUI.search_School_Login_Url(self))
        self.init_data_button.grid(row=0, column=2)

        # 提示信息
        self.init_data_tips = Label(self.init_window_name, text="Author : Qiuyelin")
        self.init_data_tips.grid(row=0, column=3, columnspan=3)
        # 点击标签打开链接
        self.init_data_tips.bind('<Button-1>', lambda event: webbrowser.open('https://github.com/pooneyy/get_Schools_Login_URL_in_DailyCP'))

        # 文本框
        self.result_data_Text = Text(self.init_window_name, width=56, height=34,font=("宋体",13))  #处理结果展示
        self.result_data_Text.grid(row=1, column=0, rowspan=15, columnspan=4)
        self.result_data_Text.insert(1.0, '\n Tips: \n\n   1.请输入学校名称，点击查询按钮即可查询\n\n   2.支持模糊搜索\n\n   3.查询到URL,双击URL可直接在浏览器打开\n\n   4.点击输入框可清空已输入内容\n\n\n\n\n\n')
        self.result_data_Text.insert(END,'________________________________________________________\n\n')
        self.result_data_Text.insert(END,'\n Author : Qiuyelin')
        self.result_data_Text.insert(END,'\n Version	: 1.0')
        self.result_data_Text.insert(END,'\n 2022.05.05   By Python 3.8.3')

    # 删除文本框控件
    def delete_Text(self):
        self.result_data_Text.grid_remove()

    def create_LineBox(self):
        # 创建列表框
        self.result_data_List = Listbox(self.init_window_name, width=54, height=32,font=("宋体",13))  #处理结果展示
        self.result_data_List.grid(row=1, column=0, rowspan=15, columnspan=4)

        # 创建滚动条
        self.result_data_Scroll = Scrollbar()  #列表框滚动条
        self.result_data_Scroll.grid(row=1, column=5, rowspan=15, sticky=N+S)
        
        # 关联列表框、滚动条
        self.result_data_Scroll.config(command=self.result_data_List.yview)
        self.result_data_List.config(yscrollcommand= self.result_data_Scroll.set)

    def search_School_Login_Url(self):
        self.create_LineBox()
        self.delete_Text()
        schoolName = self.init_data_input.get()
        response = requests.get('https://mobile.campushoy.com/v6/config/guest/tenant/list')
        data = json.loads(response.text).get('data')
        # 清空列表框
        self.result_data_List.delete(0, END)
        # self.result_data_Text.delete(1.0,END)
        sum = 0
        if schoolName == '':
            self.result_data_List.insert('1', '输入框为空')
        else:
            for i in data:
                if schoolName in i.get('name'):
                    # 如果idsUrl存在
                    if i.get('idsUrl'):
                        self.result_data_List.insert(END,f"{i.get('name')}")
                        self.result_data_List.insert(END,f"{i.get('idsUrl')}")
                        self.result_data_List.insert(END,'')
                        sum += 1
            if sum == 0:
                self.result_data_List.insert(END,f"没有找到 {schoolName} ，请检查输入是否正确")
        # 点击URL从edge浏览器打开
        self.result_data_List.bind('<Double-Button-1>', self.open_url)

    def open_url(self,event):
        line_num = self.result_data_List.curselection()      # 获取点击的行号
        line_content = self.result_data_List.get(line_num)   # 获取点击的内容
        line_content = line_content.replace('\n','')         # 去除换行符
        # 如果为URL,打开URL
        if 'http' in line_content:
            webbrowser.open(line_content)



def gui():
    init_window = Tk()          # 实例化出一个父窗口
    root = GUI(init_window)
    root.set_init_window()      # 设置根窗口默认属性
    init_window.mainloop()      # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

if __name__ == '__main__':
    gui()
