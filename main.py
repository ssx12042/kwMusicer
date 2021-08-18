# -*- coding: utf-8 -*-
# @Time    : 2021/8/17 23:45
# @Author  : Ssx
# @Email   : ssx12042@163.com
# @File    : main.py
# @Software: PyCharm


from kuwo.music import kw_search, KuWoMusic
from kuwo.music import kw_download
from tkinter import *
from tkinter import messagebox


class My_Musicer:
    def __init__(self):
        self.root = Tk()  # 初始化窗口
        self.root.title('音乐下载器_v1.0')  # 窗口名称
        self.root.geometry("900x420+10+10")  # 500x300为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        # 设置窗口是否可变，默认为True
        self.root.resizable(width=False, height=False)

        # 播放器类型块
        # 标签
        Label(self.root, text="播放器类型:").grid(row=0, column=0)
        # 单选框
        self.selected_musicer = IntVar()  # 已选的音乐播放器类型
        rad1 = Radiobutton(self.root, text="酷我", value=1, variable=self.selected_musicer)
        # rad2 = Radiobutton(self.root, text="酷狗", value=2, variable=self.selected_musicer)  # TODO
        # rad3 = Radiobutton(self.root, text="网易云", value=3, variable=self.selected_musicer)  # TODO
        rad1.select()  # 默认选择酷我
        rad1.grid(row=0, column=1, sticky=W, columnspan=4)
        # rad2.grid(row=0, column=1, columnspan=4)
        # rad3.grid(row=0, column=1, sticky=E, columnspan=4)

        # 搜索块
        # 标签
        Label(self.root, text="搜索关键字:").grid(row=1, column=0)
        # 输入框（标签高度，内容显示方式，字体大小颜色）
        self.search_entry = Entry(self.root, width=85, show=None, font=('Arial', 12))
        self.search_entry.grid(row=1, column=1, columnspan=10, sticky=W)
        # 搜索按钮
        self.search_btn = Button(self.root, text="搜索", command=self.search)
        self.search_btn.grid(row=2, column=1, columnspan=10)

        # 分隔
        Label(self.root).grid(row=3, column=1)

        # 搜索结果块
        # 标签
        Label(self.root, text="序号").grid(row=4, column=1, sticky=W, columnspan=2)
        Label(self.root, text="歌名").grid(row=4, column=2, sticky=W, columnspan=2)
        Label(self.root, text="歌手").grid(row=4, column=4, columnspan=2)
        Label(self.root, text="时长(s)").grid(row=4, column=5, sticky=E, columnspan=2)
        Label(self.root, text="专辑").grid(row=4, column=8, sticky=W, columnspan=2)
        Label(self.root, text="搜索结果:").grid(row=5, column=0)
        # 创建列表框
        self.res_list = Listbox(self.root, width=110, height=10)  # 创建列表框组件，用于展示搜索结果
        self.res_list.grid(row=5, column=1, columnspan=10, sticky=W)

        # 分隔
        Label(self.root).grid(row=6, column=1)

        # 下载块
        # 标签
        Label(self.root, text="下载歌曲的序号:").grid(row=7, column=0)
        # 输入框（标签高度，内容显示方式，字体大小颜色）
        self.num_entry = Entry(self.root, width=86, show=None, font=('Arial', 12))
        self.num_entry.grid(row=7, column=1, columnspan=10, sticky=W)
        # 下载按钮
        self.download_btn = Button(self.root, text="下载", command=self.download)
        self.download_btn.grid(row=8, column=1, columnspan=10)

        # 下载结果
        self.download_res = Label(self.root)
        self.download_res.grid(row=9, column=1, columnspan=10)

        self.root.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

    def search(self):
        '''
        使用关键字进行歌曲信息搜索
        :return: null
        '''
        # 实例创建
        self.kw = KuWoMusic()  # 酷我实例
        self.info_list = []  # 存放搜索结果(带音乐id)
        self.info_list_GUI = []  # 存放详细搜索结果(不带音乐id)

        search_info = self.search_entry.get().strip()  # 获取搜索的关键字，并去除头尾的空格
        if search_info == "":
            messagebox.showinfo("错误", "请输入搜索关键字（歌曲名称或歌手名字）")
            return
        self.res_list.delete(0, END)  # 清空list
        musicer = self.selected_musicer.get()  # 获取已选择的播放器类型
        if musicer == 1:  # 酷我
            self.info_list, self.info_list_GUI = kw_search(search_info, self.kw)
        elif musicer == 2:  # 酷狗
            pass
            # kg_main()  # TODO
        elif musicer == 3:  # 网易云
            pass
            # wyy_main()  # TODO

        for item in self.info_list_GUI:  # 插入数据到listbox
            s = '{0:{5}<5}{1:{5}<20}{2:{5}<10}{3:{5}<10}{4:{5}<20}' \
                .format(item[0] + 1, item[1], item[2], item[3], item[4], chr(12288))
            self.res_list.insert(END, s)  # 向listbox的尾部添加数据

    def download(self):
        '''
        根据搜索出来歌曲序号下载对应歌曲
        :return: null
        '''
        if len(self.info_list) == 0:
            messagebox.showinfo("错误", "请先进行歌曲信息搜索")
            return
        num = self.num_entry.get().strip()  # 获取输入的歌曲序号，并去除头尾的空格
        if num == "" or not str(num).isdigit() or not 1 <= int(num) <= 10:
            messagebox.showinfo("错误", "请输入要下载歌曲的序号(1~10)")
            return
        else:
            flag = kw_download(self.info_list[int(num) - 1], self.kw)
            if flag:
                self.download_res.config(text=self.info_list[int(num) - 1][1] + "下载成功！")


if __name__ == '__main__':
    My_Musicer()
