# -*- coding: utf-8 -*-
# Author:  @ MuLun_Zhu
# @Time :  2020/8/23 10:46 上午

import re
import tkinter
import tkinter.messagebox
import tkinter.ttk
import traceback

import pro_sql

"""
sql弹窗错误：sql函数try语句
输入格式错误：check函数re匹配
数据错误(sql中无对应数据)：。。。
"""

PHONE_RE = r"^1[345789][0-9]{9}$"
PASSWORD_RE = r"[a-z0-9A-Z]{6,16}$"
SPACE_RE = "^ {0,10}$"  # 匹配多个空格
NUM_RE = "[0-9]+"

# base_path = sys._MEIPASS
"""
重要的事情多说几遍 windows系统请将base_path中 正斜杠 改为 反斜杠 
重要的事情多说几遍 windows系统请将base_path中 正斜杠 改为 反斜杠 
重要的事情多说几遍 windows系统请将base_path中 正斜杠 改为 反斜杠 
重要的事情多说几遍 windows系统请将base_path中 正斜杠 改为 反斜杠 
"""
base_path = "\\"
"""
重要的事情多说几遍 windows系统请将base_path中 正斜杠 改为 反斜杠 
重要的事情多说几遍 windows系统请将base_path中 正斜杠 改为 反斜杠 
重要的事情多说几遍 windows系统请将base_path中 正斜杠 改为 反斜杠 
重要的事情多说几遍 windows系统请将base_path中 正斜杠 改为 反斜杠 
"""


# hostname = socket.gethostname()
# ip = socket.gethostbyname(hostname)


class Window(object):
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry("550x400")
        self.root.resizable(width=False, height=False)
        self.root["background"] = "#8b98a7"
        self.root.iconbitmap("." + base_path + "leaf.ico")
        self.root.title("智能土壤养分监测系统aV1.2", )
        self.root.protocol("WM_DELETE_WINDOW", self.close_handle)  # 窗体关闭协议
        # 用于窗口刷新
        self.main_frame = 1
        self.right_frame = 1
        # 用于SQL语句判断
        self.sql_judge = 0  # 注册1 登录2 修改密码3 设置昵称4
        # 合法性检查
        self.permit_phone = False  # 账号合法性
        self.permit_password = False  # 密码合法性
        self.permit_in = False  # 密码和账号综合合法性检查
        self.menu_in = True  # 先许可使用菜单，退出登录时设为false，在昵称，正向，反向搜索页有判断，TRUE才可以进入
        self.sign_out_delete = False  # 退出登录时，防止预填写，判断为TRUE则删除预填写
        # 在searchforplant接受ph_light_combobox内容，借此传给其他函数 否则AttributeError: 'Window' object has no attribute 'type_combobox'
        self.ph_Var = tkinter.StringVar()
        self.light_Var = tkinter.StringVar()
        # 用于check_key函数判断搜索或者提交数据
        self.search_or_sub = False
        # 用于筛选函数，forplant or forenvironment  1是plant，2是environment
        self.for_plant_or_for_environment = False
        # 筛选函数和for plant 函数中，sql查询需要最终输入的多个字符
        self.final_key_list = []
        self.units = [" ", " ", "°c", "%rh", "S/m", "mg/kg", "mg/kg", "mg/kg"]
        self.type = ["pH范围", "光照条件", "温度", "湿度", "电导率", "氮浓度", "磷浓度", "钾浓度"]
        self.type_plus = ["物种名称", "类别", "pH范围", "光照条件", "温度", "湿度", "电导率", "氮浓度", "磷浓度", "钾浓度"]
        self.type_list = ["花卉", "果蔬", "水生", "树木"]
        self.light_tuple_all = ("all", "少(完全室内)", "偏少", "正常(仅上午或下午)", "偏多", "多(全天无遮挡)")
        self.light_tuple_unknow = ("未知", "少(完全室内)", "偏少", "正常(仅上午或下午)", "偏多", "多(全天无遮挡)")
        self.username = tkinter.StringVar()  # 电话号码
        self.username.set("建议使用手机号")
        self.nickname = tkinter.StringVar()  # 用于修改昵称  初始化昵称
        self.password = tkinter.StringVar()  # 密码

        self.pw_tip = tkinter.StringVar()  # 用于密码即时检查的 提示
        self.pw_tip.set(" ")
        self.phone_number = tkinter.StringVar()  # 用于号码即时检查的 提示
        self.phone_number.set(" ")

        self.main_label = tkinter.Label(self.root, text='智能土壤养分监测系统V1.2', bg="#8b98a7", fg="#222222", font=("微软雅黑", 10))
        self.main_label.pack(anchor=tkinter.NW, side=tkinter.TOP)
        self.sign()
        # 更改下拉框默认颜色
        combostyle = tkinter.ttk.Style()
        combostyle.theme_create('combostyle', parent='alt',
                                settings={'TCombobox':
                                              {'configure':
                                                   {'foreground': '#222222',
                                                    'selectbackground': '#9ba8b7',
                                                    'fieldbackground': '#9ba8b7',
                                                    'background': '#9ba8b7',
                                                    'font': 10
                                                    }}}
                                )
        combostyle.theme_use('combostyle')
        self.root.mainloop()

    # 关闭程序
    def close_handle(self):
        if tkinter.messagebox.askyesnocancel("关闭程序", "确认退出？\n当前检索历史将清空！"):
            pro_sql.close_db_and_cur()
            self.root.destroy()

    # 登录
    def sign(self):
        self.sql_judge = 2
        if self.main_frame != 1:
            self.main_frame.destroy()
        self.main_frame = tkinter.Frame(self.root, bg="#8b98a7")  # 创建Frame
        self.main_frame.pack(anchor=tkinter.CENTER, fill=tkinter.Y, expand=tkinter.YES, pady=45)
        tkinter.Label(self.main_frame, bg="#8b98a7", fg="#222222").grid(row=1)
        # 登录
        self.big_label = tkinter.Label(self.main_frame, text='智能土壤养分监测系统V1.2', bg="#8b98a7", fg="#222222",
                                       font=("微软雅黑", 15))
        self.big_label.grid(row=0, padx=10, pady=20, column=1, )

        tkinter.Label(self.main_frame, text='账户: ', font=("微软雅黑", 13), bg="#8b98a7", fg="#222222").grid(row=1, pady=3)
        self.account_entry = tkinter.Entry(self.main_frame, textvariable=self.username, width=20, bg="#dddddd",
                                           fg='#333333', font=("微软雅黑", 12))
        self.account_entry.bind(sequence="<Button-1><ButtonRelease-1>", func=self.choose_account_text)
        self.account_entry.bind("<KeyRelease>", self.check_account_phone_number)
        self.account_entry.grid(row=1, column=1, pady=3)
        tkinter.Label(self.main_frame, textvariable=self.phone_number, bg="#8b98a7", fg="#222222",
                      font=("微软雅黑", 10), ).grid(row=2, column=1)
        tkinter.Label(self.main_frame, text='密码: ', bg="#8b98a7", fg="#222222", font=("微软雅黑", 13), ).grid(row=3, pady=0)
        self.pwentry = tkinter.Entry(self.main_frame, textvariable=self.password, width=20, show='*', bg="#dddddd",
                                     fg='#333333', font=("微软雅黑", 12))
        self.pwentry.bind("<Return>", self.sql_split)
        self.pwentry.bind("<KeyRelease>", self.check_password)
        self.pwentry.grid(row=3, column=1, pady=0)
        tkinter.Label(self.main_frame, textvariable=self.pw_tip, bg="#8b98a7", fg="#222222", font=("微软雅黑", 10), ).grid(
            row=4, column=1)
        self.login = tkinter.Button(self.main_frame, text='登陆', font=("微软雅黑", 10), height=1, bd=1, bg="#8b98a7",
                                    fg="#222222", activebackground="#9ba8b7", width=17)
        self.login.bind("<Button-1>", self.sql_split)
        self.login.grid(row=5, pady=10, padx=10, column=1)
        # 注册
        self.label = tkinter.Label(self.main_frame, text='注册', fg="#0000ff", bg="#8b98a7",
                                   font=("微软雅黑", 12, "underline"))
        self.label.bind("<Button-1>", self.register)
        self.label.grid(row=5, column=0)
        # 忘记密码?
        self.label = tkinter.Label(self.main_frame, text='忘记密码?', fg="#0000ff", bg="#8b98a7",
                                   font=("微软雅黑", 8, "underline"))
        self.label.bind("<Button-1>", self.change_password)
        self.label.grid(row=5, column=2)
    def sign_with_event(self, event):
        self.sign()

    # 注册页
    def register(self, event):
        self.sql_judge = 1
        if self.main_frame != 1:
            self.main_frame.destroy()
        self.main_frame = tkinter.Frame(self.root, bg="#8b98a7")  # 创建Frame
        self.main_frame.pack(pady=60)
        tkinter.Label(self.main_frame, text="注册账号", font=("微软雅黑", 15),
                      bg="#8b98a7", fg="#222222").grid(row=0, column=0, columnspan=2, padx=20, pady=10)
        tkinter.Label(self.main_frame, text='账户:     ', font=("微软雅黑", 13), bg="#8b98a7").grid(row=1, pady=3)
        self.account_r_entry = tkinter.Entry(self.main_frame, textvariable=self.username, bg="#dddddd",
                                             font=("微软雅黑", 12))
        self.account_r_entry.bind(sequence="<Button-1><ButtonRelease-1>", func=self.delete_r_account_text)
        self.account_r_entry.bind("<KeyRelease>", self.check_account_phone_number)
        self.account_r_entry.grid(row=1, column=1, )
        tkinter.Label(self.main_frame, textvariable=self.phone_number, bg="#8b98a7", fg="#222222",
                      font=("微软雅黑", 10), ).grid(row=2, column=1)

        tkinter.Label(self.main_frame, text='密码:     ', font=("微软雅黑", 13), bg="#8b98a7").grid(row=3, pady=3)
        self.pwentry = tkinter.Entry(self.main_frame, textvariable=self.password, show='*', bg="#dddddd",
                                     font=("微软雅黑", 12))
        if self.sign_out_delete:
            print("delete")
            self.delete_pw_text()
        self.pwentry.bind("<KeyRelease>", self.check_password)
        self.pwentry.bind("<Return>", self.sql_split)
        self.pwentry.grid(row=3, column=1)
        tkinter.Label(self.main_frame, textvariable=self.pw_tip, bg="#8b98a7", fg="#222222", font=("微软雅黑", 10), ).grid(
            row=4, column=1)
        self.already_have_an_account_label = tkinter.Label(self.main_frame, text='已有账号', fg="#0000ff", bg="#8b98a7",
                                                           font=("微软雅黑", 10, "underline"))
        self.already_have_an_account_label.bind("<Button-1>", self.sign_with_event)
        self.already_have_an_account_label.grid(row=4, column=0)

        self.register_and_signin = tkinter.Button(self.main_frame, text='注册并登陆', font=("微软雅黑", 13), bg="#8b98a7",
                                                  fg="#aa0000", )
        self.register_and_signin.bind("<Button-1>", self.sql_split)
        self.register_and_signin.grid(row=5, column=0, columnspan=2, pady=10)

    # 改密码
    def change_password(self, event):
        self.change_password_in_menu_without_event()
    def change_password_in_menu_without_event(self):
        self.sql_judge = 3
        if self.main_frame != 1:
            self.main_frame.destroy()
        self.main_frame = tkinter.Frame(self.root, bg="#8b98a7")  # 创建Frame
        self.main_frame.pack(anchor=tkinter.CENTER, fill=tkinter.Y, expand=tkinter.YES, pady=60)
        tkinter.Label(self.main_frame, text="修改密码", font=("微软雅黑", 15),
                      bg="#8b98a7", fg="#222222").grid(row=0, column=0, columnspan=2, padx=50, pady=20)
        tkinter.Label(self.main_frame, text='账户:      ', font=("微软雅黑", 13), bg="#8b98a7").grid(row=1, pady=10, column=0)
        self.account_entry = tkinter.Entry(self.main_frame, textvariable=self.username, bg="#dddddd", fg="#222222",
                                           font=("微软雅黑", 12))
        self.account_entry.bind(sequence="<Button-1><ButtonRelease-1>", func=self.choose_account_text)
        self.account_entry.bind("<KeyRelease>", self.check_account_phone_number)
        self.account_entry.grid(row=1, column=1, )
        tkinter.Label(self.main_frame, text='新密码:  ', font=("微软雅黑", 13), bg="#8b98a7", fg="#222222").grid(row=2,
                                                                                                          pady=5,
                                                                                                          column=0)
        self.pwentry = tkinter.Entry(self.main_frame, textvariable=self.password, show='*', bg="#dddddd",
                                     font=("微软雅黑", 12))
        self.pwentry.bind("<Return>", self.sql_split_without_event)
        self.pwentry.bind("<KeyRelease>", self.check_password)
        self.pwentry.grid(row=2, column=1)

        self.sign_label = tkinter.Label(self.main_frame, text='已有账号', fg="#0000ff", bg="#8b98a7",
                                        font=("微软雅黑", 10, "underline"))
        self.sign_label.bind("<Button-1>", self.sign_with_event)
        self.sign_label.grid(row=3, column=0)

        self.button = tkinter.Button(self.main_frame, text='提交/登陆', width=11, bd=1, fg="#222222", bg="#8b98a7",
                                     font=("微软雅黑", 13),
                                     command=self.sql_split_without_event)
        self.button.grid(row=4, column=0, columnspan=2, rowspan=2, pady=1, padx=40)

    # 分流函数之一 处理 注册 相关内容
    def sql_register(self):
        try:
            success = pro_sql.registersql(self.username.get(), self.password.get())
        except Exception as result:
            print(result)
            tkinter.messagebox.showinfo("sql", "registerERROR:此账号已被注册 或者 网络繁忙")
        else:
            if success:  # 如果try代码正确但是数据库没有相关账户数据，success就为0
                tkinter.messagebox.showinfo("提示", "注册成功")
                self.search_the_environment()
            else:
                tkinter.messagebox.showinfo("提示", "warning: 网络繁忙，请重试\nwarning: 网络繁忙，请重试\nwarning: 网络繁忙，请重试")
                print("注册sql数据错误")

    # 分流函数之一 处理 登录 相关内容
    def sql_sign(self):
        try:
            success = pro_sql.signsql(self.username.get(), self.password.get()) # 密码是否正确？？？
            is_pwd = pro_sql.sign_sql_account_exist(self.username.get()) # 账号是否存在？？？
        except Exception as result:
            print(result)
            tkinter.messagebox.showinfo("sql", "loginERROR：网络繁忙")
        else:
            if success == 'ok':  # 账号和密码都对
                self.menu_in = True
                self.search_the_environment()
            else:  # 如果try代码正确但是数据库没有相关账户数据，success就为0
                if is_pwd == "yes":
                    tkinter.messagebox.showinfo("提示", "warning: 密码错误\nwarning: 密码错误\nwarning: 密码错误")
                    print("密码错误")
                else:
                    tkinter.messagebox.showinfo("提示", "warning: 网络繁忙 或者 未注册")

    # 分流函数之一 处理 密码更新 相关内容
    def sql_password(self):
        try:
            success = pro_sql.pwdsql(self.username.get(), self.password.get())
        except Exception as result:
            print(result)
            tkinter.messagebox.showinfo("sql", "updateERROR：网络繁忙")
        else:
            if success:  # 如果try代码正确但是数据库没有相关账户数据，success就为0
                tkinter.messagebox.showinfo("提示", "更新成功")
                self.menu_in = True
                self.search_the_environment()
            else:
                tkinter.messagebox.showinfo("提示", "warning: 未注册账号或密码重复\nwarning: 未注册账号或密码重复\nwarning: 未注册账号或密码重复")
                print("更改密码sql数据错误")

    # 分流函数之一 处理 昵称修改 相关内容
    def sql_change_nickname(self):
        try:
            success = pro_sql.nickname_change_sql(self.username.get(), self.nickname.get())
        except Exception as result:
            print(result)
            tkinter.messagebox.showinfo("sql", "changeERROR：网络繁忙")
        else:
            if success:  # 如果try代码正确但是数据库没有相关账户数据，success就为0
                self.search_the_environment()
            else:
                tkinter.messagebox.showinfo("提示", "warning: 昵称太长，请重试\nwarning: 网络繁忙，请重试\nwarning: 请重试")
                print("更改昵称sql数据错误")

    # 输入植物搜索环境
    def sql_search_for_environment(self):
        try:
            self.info = pro_sql.search_for_environment(self.plant_name_content.get())
            self.for_plant_or_for_environment = 1  # 筛选函数区分来源
        except Exception as result:
            print(result)
            tkinter.messagebox.showinfo("sql", "searchERROR：网络繁忙")
        else:  # 没发生异常
            if self.info == 0:
                tkinter.messagebox.showinfo("提示", "抱歉：未找到相关数据")
            elif isinstance(self.info, list):
                self.show_base_plant_without_event()
    def sql_search_for_environment_without_event(self, event):
        self.sql_search_for_environment()

    # 电话号码检验
    def check_account_phone_number(self, event):
        phone_number = self.username.get()
        print(phone_number)
        if re.match(PHONE_RE, phone_number):
            self.phone_number.set(" " * 50)
            self.permit_phone = True
            print("ok")
            if self.permit_password == True:
                self.permit_in = True
        else:
            self.phone_number.set("请使用大陆手机号")
            self.permit_phone = False

    # 密码检验
    def check_password(self, event):
        self.permit_in = False
        password = self.password.get()
        print(password)
        if re.match(PASSWORD_RE, password):
            self.pw_tip.set(" " * 50)
            print("ok")
            self.permit_pssword = True
            if self.permit_phone == True:
                self.permit_in = True
        else:
            self.pw_tip.set("6-16位，请勿使用特殊字符")
            self.permit_pssword = False

    # 提交数据检验
    def check_sub_key(self, event):
        Var_list = []
        print("Var_list == ", end="")
        Var_list = [self.ph_.get(), self.temp_.get(), self.rh_.get(), self.sm_.get(), self.n_.get(), self.p_.get(),
                    self.k_.get()]
        print(Var_list)
        # 检验输入是否合法 字母与空格数字混合
        str_list = []
        for item in Var_list:
            if re.match(SPACE_RE, item):
                str_list.append(0)
                continue
            elif item in self.units[2:]:
                str_list.append(0)
                continue
            elif (" " in item and re.search(NUM_RE, item)) or re.search("[a-zA-z]", item):
                tkinter.messagebox.showinfo("提示", str(item) + " 输入格式错误")
                return
            else:
                str_list.append(item)
        if str_list[0] == 0:  # 如果ph值没有输入就默认为 未知
            str_list[0] = "未知"
        print(str_list)
        name_and_type_list = [self.name_.get(), self.type_.get(), self.light_.get()]
        print(name_and_type_list)
        # 名字里面不能有空格，类别只能是四选一
        if " " in name_and_type_list[0] or name_and_type_list[1] not in self.type_list or name_and_type_list[0] in ["",
                                                                                                                    "无名"]:
            tkinter.messagebox.showinfo("错误", "名称或类别填写不规范")
            return
        final_sub_list = []
        for item in name_and_type_list:
            final_sub_list.append(item)
        for item in str_list:
            final_sub_list.append(float(item))
        print(final_sub_list)
        try:
            info = pro_sql.submit_info(final_sub_list)
            if info == 0:
                tkinter.messagebox.showerror("提示", "网络繁忙")
                return
            elif info == 1:
                tkinter.messagebox.showinfo("提示", "success：插入成功\nsuccess：插入成功\nsuccess：插入成功")
        except Exception as result:
            print(result)

    # 反向检索检验
    def check_search_key(self, event):
        Var_list = []
        print("Var_list == ", end="")
        Var_list = [self.temp.get(), self.rh.get(), self.sm.get(), self.n.get(), self.p.get(), self.k.get()]
        print(Var_list)
        # 检验输入是否合法 字母与空格数字混合
        str_list = []
        for item in Var_list:
            if re.match(SPACE_RE, item):
                str_list.append(5000)
                continue
            elif item in self.units[2:]:
                str_list.append(5000)
                continue
            elif (" " in item and re.search(NUM_RE, item)) or re.search("[a-zA-z]", item):
                tkinter.messagebox.showinfo("提示", str(item) + " 输入格式错误")
                return
            else:
                str_list.append(item)
        print("str_list == ", end="")
        print(str_list)
        # 转int
        self.final_key_list = []
        if self.ph_Var.get() == "" or self.ph_Var.get() == "all":  # 未选择时，此var为""
            self.ph_Var.set("%")
        if self.light_Var.get() == "" or self.light_Var.get() == "all":
            self.light_Var.set("%")
        self.final_key_list.append(self.ph_Var.get())
        self.final_key_list.append(self.light_Var.get())
        for item in str_list:
            try:
                self.final_key_list.append(float(item))
            except Exception as result:
                print(result)
                tkinter.messagebox.showinfo("提示", str(item) + "输入格式错误")
                return
            else:
                print("合法" + str(item))

        print(self.final_key_list)
        try:
            self.info = pro_sql.search_for_plant_sql(self.final_key_list)
            self.for_plant_or_for_environment = 2  # 筛选函数需要
            if self.info == 0:
                tkinter.messagebox.showinfo("提示", "抱歉，没找到相关数据 或者 网络繁忙")
                return
            self.show_base_plant_without_event()
        except Exception as result:
            print(result)

    # 检查账号密码合法性（电话号码，密码长度等等），然后信息分流
    def sql_split_without_event(self):
        if self.permit_in == False:
            tkinter.messagebox.showinfo("提示", "warning：账号或密码格式错误！\nwarning：账号或密码格式错误！\nwarning：账号或密码格式错误！")
            return
        name = self.username.get()
        secret = self.password.get()
        if self.sql_judge == 1:
            self.sql_register()
        if self.sql_judge == 2:
            self.sql_sign()
        if self.sql_judge == 3:
            self.sql_password()
        if self.sql_judge == 4:
            self.sql_change_nickname()
    def sql_split(self, event):
        self.sql_split_without_event()

    # 测试需要，直接许可,进入搜索环境页
    def direct_in(self, event):
        self.menu_in = True
        self.search_the_environment()

    # 输入植物，检索环境
    def search_the_environment(self):
        if self.menu_in == False:
            self.out_of_menu()
            return
        self.create_menu()
        self.show_nickname()
        if self.main_frame != 1:
            self.main_frame.destroy()
        self.main_frame = tkinter.Frame(self.root, bg="#8b98a7")
        self.plant_name_content = tkinter.StringVar()
        self.plant_name_content.set("请输入植物名")
        self.plant_entry = tkinter.Entry(self.main_frame, width=20, font=("微软雅黑", 13,), bg="#dddddd",
                                         highlightcolor="#0000ff",
                                         textvariable=self.plant_name_content)  # 单行输入
        self.plant_entry.bind(sequence="<Button-1><ButtonRelease-1>", func=self.delete_plant_text)
        self.plant_entry.bind("<Return>", self.sql_search_for_environment_without_event)
        self.plant_entry.grid(row=1, column=0)
        self.button = tkinter.Button(self.main_frame, text="查询生长环境", font=("微软雅黑", 13,), bg="#8b98a7", fg="#222222",
                                     command=self.sql_search_for_environment)
        self.button.grid(row=4, column=0, pady=30)
        self.main_frame.pack(anchor=tkinter.CENTER, pady=100)

    # 显示搜索结果页面的 基础信息
    def show_base_plant_without_event(self):
        if self.main_frame != 1:
            self.main_frame.destroy()
        self.main_frame = tkinter.Frame(self.root, bg="#8b98a7", )
        self.main_frame.pack(anchor=tkinter.CENTER, fill=tkinter.BOTH, padx=80)
        self.left_frame = tkinter.Frame(self.main_frame, bg="#8b98a7", )
        self.left_frame.grid(row=1, column=1, pady=10)
        # 下拉框
        self.nw_frame = tkinter.Frame(self.left_frame, bg="#8b98a7")
        self.nw_frame.pack(side=tkinter.TOP, pady=10)
        # 筛选
        type_tuple = ("所有", "花卉", "果蔬", "水生", "树木")
        self.type_combobox = tkinter.ttk.Combobox(self.nw_frame, values=type_tuple, width=13, )
        self.type_combobox.bind("<<ComboboxSelected>>", self.sql_select_handle)
        # 下拉框默认值
        self.type_combobox.current(0)
        self.type_combobox.grid(row=0, column=0, columnspan=2)
        # 显示筛选条件
        self.filtrate_content = tkinter.StringVar()
        self.filtrate_content.set(" ")
        tkinter.Label(self.nw_frame, text="筛选条件：", bg="#8b98a7", fg="#222222").grid(row=1, column=0)
        self.label = tkinter.Label(self.nw_frame, textvariable=self.filtrate_content, bg="#8b98a7", fg="#222222", )
        self.label.grid(row=1, column=1)
        # 滚动条
        self.gun_frame = tkinter.Frame(self.left_frame)
        self.gun_frame.pack(side=tkinter.TOP)
        self.scrollbar = tkinter.Scrollbar(self.gun_frame, bg="#8b98a7")
        self.listbox = tkinter.Listbox(self.gun_frame, height=13, width=17, yscrollcommand=self.scrollbar.set,
                                       font=("微软雅黑", 10,), bg="#dddddd", )
        self.listbox.delete(0, tkinter.END)
        print(self.info)
        if self.info != 0:  # 在没有数据的情况下,0没有迭代功能
            for index, item in enumerate(self.info):
                self.listbox.insert("end", "「{info:0>3}」{name}".format(info=index, name=item[0]))

        self.listbox.bind("<Double-Button-1>", self.show_specific_info)
        # 图片
        self.img = tkinter.PhotoImage(file="." + base_path + "arrow_3.png")
        tkinter.Label(self.main_frame, image=self.img, bg="#8b98a7", fg="#222222").grid(row=1, column=2)
        # 导入mysql数据
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side="right", fill="y", )
        self.listbox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        # 八个标签label——frame
        self.mid_frame = tkinter.Frame(self.main_frame, bg="#8b98a7")
        self.mid_frame.grid(row=1, column=3)

        row_un_empty = [2, 4, 6, 8, 10, 12, 14, 16]
        row_empty = [1, 3, 5, 7, 9, 11, 13, 15]
        for type, empty, un_empty in zip(self.type, row_empty, row_un_empty):
            self.str = tkinter.StringVar()
            self.str.set("%s" % type)
            tkinter.Label(self.mid_frame, textvariable=self.str, bg="#8b98a7", fg="#222222", ).grid(row=un_empty,
                                                                                                    sticky='w', pady=7)
    def show_base_plant(self, event):
        self.show_base_plant_without_event()

    # 处理正向筛选
    def sql_select_handle(self, event):
        if self.type_combobox.get() == "所有":
            self.show_base_plant_without_event()
            return
        self.filtrate_content.set(self.type_combobox.get())
        if self.for_plant_or_for_environment == 1:
            filtrate_list = pro_sql.filtrate(self.plant_name_content.get(), self.filtrate_content.get())
        if self.for_plant_or_for_environment == 2:
            filtrate_list = pro_sql.filtrate_for_plant_sql(self.final_key_list, self.filtrate_content.get())
        if isinstance(filtrate_list, list):
            self.listbox.delete(0, tkinter.END)
            for index, item in enumerate(filtrate_list):
                self.listbox.insert(tkinter.END, "「{info:0>3}」".format(info=index) + str(item[0]))
        elif filtrate_list == 0:
            self.listbox.delete(0, tkinter.END)

    #  显示搜索结果页详情
    def show_specific_info(self, event):
        # 在self.info二维列表中找正确的列表
        for index in self.listbox.curselection():
            print("index == " + str(index))
            for item in self.info:
                if self.listbox.get(index)[5:] in item:  # 由于显示的时候存在序号修饰，所以需要切片再提交查询
                    self.row_info = item[2:]
                    break
                else:
                    print("%s寻找数据中 > 对选择的box切片结果" % len(self.info), end=" ")
                    print(self.listbox.get(index)[5:])

        if self.right_frame != 1:
            self.right_frame.destroy()
        self.right_frame = tkinter.Frame(self.main_frame, bg="#8b98a7")
        self.right_frame.grid(row=1, column=4)
        row_un_empty = [2, 4, 6, 8, 10, 12, 14, 16]
        row_empty = [1, 3, 5, 7, 9, 11, 13, 15]

        for unit, empty, un_empty, info in zip(self.units, row_empty, row_un_empty, self.row_info):
            self.str = tkinter.StringVar()
            self.str.set(" %s %s" % (info, unit))
            tkinter.Label(self.right_frame, textvariable=self.str, bg="#8b98a7", fg="#222222", ).grid(row=un_empty,
                                                                                                      column=1,
                                                                                                      sticky='w',
                                                                                                      pady=7)

    # insert data 提交数据用
    def set_Var_type_(self, event):
        self.type_.set(self.type_combobox.get())
    def set_Var_light_(self, event):
        self.light_.set(self.light_combobox.get())

    # 提交数据
    def commit_info(self):
        if self.menu_in == False:
            self.out_of_menu()
            return
        if self.main_frame != 1:
            self.main_frame.destroy()
        self.main_frame = tkinter.Frame(self.root, bg="#8b98a7")
        self.main_frame.pack(anchor=tkinter.CENTER)
        self.the_frame = tkinter.Frame(self.main_frame, bg="#8b98a7")
        self.the_frame.pack(ipadx=1, pady=25)
        self.type_plus = ["物种名称", "类别", "pH范围", "光照条件", "温度", "湿度", "电导率", "氮浓度", "磷浓度", "钾浓度"]

        rowslist = [0, 0, 4, 2, 6, 2, 4, 6, 8, 8]
        columnlist = [0, 3, 0, 0, 0, 3, 3, 3, 0, 3]
        for type, row, column in zip(self.type_plus, rowslist, columnlist):
            self.light_label = tkinter.Label(self.the_frame, text=type, bg="#8b98a7", fg="#222222", ).grid(row=row,
                                                                                                           column=column)
        # 设置name和type
        self.name_ = tkinter.StringVar()
        self.name_.set("无名")
        self.type_ = tkinter.StringVar()
        self.type_.set("")
        self.light_ = tkinter.StringVar()
        self.light_.set("")

        self.type_combobox = tkinter.ttk.Combobox(self.the_frame, values=self.type_list, width=10)
        self.type_combobox.bind("<<ComboboxSelected>>", self.set_Var_type_)
        self.type_combobox.grid(row=0, column=4, pady=10)

        self.light_combobox = tkinter.ttk.Combobox(self.the_frame, values=self.light_tuple_unknow, width=15)
        self.light_combobox.bind("<<ComboboxSelected>>", self.set_Var_light_)
        self.light_combobox.grid(row=2, column=1, pady=10)

        # Entry
        self.temp_ = tkinter.StringVar()
        self.temp_.set("°c")
        self.rh_ = tkinter.StringVar()
        self.rh_.set("%rh")
        self.sm_ = tkinter.StringVar()
        self.sm_.set("S/m")
        self.n_ = tkinter.StringVar()
        self.n_.set("mg/kg")
        self.p_ = tkinter.StringVar()
        self.p_.set("mg/kg")
        self.k_ = tkinter.StringVar()
        self.k_.set("mg/kg")
        self.ph_ = tkinter.StringVar()
        self.ph_.set("7")

        self.rh_entry_ = tkinter.Entry(self.the_frame, width=10, textvariable=self.rh_)
        self.sm_entry_ = tkinter.Entry(self.the_frame, width=10, textvariable=self.sm_)
        self.temp_entry_ = tkinter.Entry(self.the_frame, width=10, textvariable=self.temp_)
        self.n_entry_ = tkinter.Entry(self.the_frame, width=10, textvariable=self.n_)
        self.p_entry_ = tkinter.Entry(self.the_frame, width=10, textvariable=self.p_)
        self.k_entry_ = tkinter.Entry(self.the_frame, width=10, textvariable=self.k_)
        self.name_entry_ = tkinter.Entry(self.the_frame, width=15, textvariable=self.name_)
        self.ph_entry_ = tkinter.Entry(self.the_frame, width=10, textvariable=self.ph_)

        self.temp_entry_.grid(row=6, column=1, pady=10)
        self.rh_entry_.grid(row=2, column=4, pady=10)
        self.sm_entry_.grid(row=4, column=4, pady=10)
        self.n_entry_.grid(row=6, column=4, pady=10)
        self.p_entry_.grid(row=8, column=1, pady=10)
        self.k_entry_.grid(row=8, column=4, pady=10)
        self.name_entry_.grid(row=0, column=1, pady=10)
        self.ph_entry_.grid(row=4, column=1, pady=10)
        # 查询
        self.submit_button = tkinter.Button(self.the_frame, text="提交真实信息", font=("微软雅黑", 12), bg="#8b98a7",
                                            fg="#2b3fff", )
        self.search_or_sub = "sub"
        self.submit_button.bind("<Button-1>", self.check_sub_key)
        self.submit_button.grid(row=9, column=1, columnspan=4, pady=20)

    # 创建右键等菜单
    def create_menu(self):
        self.menu = tkinter.Menu(self.root)
        self.menu_list = tkinter.Menu(self.menu, tearoff=False)
        # 用户
        self.menu_list.add_command(label="提交数据", command=self.commit_info)
        self.menu_list.add_command(label="修改昵称", command=self.set_nickname)
        self.menu_list.add_command(label="修改密码", command=self.change_password_in_menu_without_event)
        self.menu_list.add_command(label="退出登录", command=self.sign_out)
        self.menu_list.add_separator()
        self.menu_list.add_command(label="反馈", command=self.sign)
        self.menu.add_cascade(label="用户", menu=self.menu_list)
        # 查询
        self.edit_menus = tkinter.Menu(self.menu, tearoff=False)
        self.edit_menus.add_command(label="正向查询", command=self.search_the_environment)
        self.menu_list.add_separator()
        self.edit_menus.add_command(label="反向查询", command=self.search_the_plants)
        self.menu.add_cascade(label="查询", menu=self.edit_menus)
        # 配置显示
        self.root.config(menu=self.menu)
        # 右键
        self.pop_menu = tkinter.Menu(self.root, tearoff=False)
        self.pop_menu.add_command(label="提交数据", command=self.commit_info)
        self.pop_menu.add_command(label="反向查询", command=self.search_the_plants)
        self.pop_menu.add_command(label="正向查询", command=self.search_the_environment)
        self.pop_menu.add_separator()
        self.pop_menu.add_command(label="修改昵称", command=self.set_nickname)
        self.permit_in = True
        self.pop_menu.add_command(label="修改密码", command=self.change_password_in_menu_without_event)
        self.pop_menu.add_command(label="退出登录", command=self.sign_out)
        self.pop_menu.add_separator()
        self.pop_menu.add_command(label="全局设置", command=self.tip)
        self.root.bind("<Button-3>", self.popup_handle)
        self.root.bind("<Button-1>", self.nothing)

    # 退出登录
    def sign_out(self):
        self.permit_in = False
        self.menu_in = False
        self.sign_out_delete = True
        self.nickname_label.destroy()
        self.sign()

    # 退出登录将无法使用菜单
    def out_of_menu(self):
        tkinter.messagebox.showinfo("提示", "请先登录")

    # todo 希望可以单击取消对entry的锁定 1.3
    def nothing(self, event):
        pass

    # 反向搜索，根据环境搜索植物
    def search_the_plants(self):
        if self.menu_in == False:
            self.out_of_menu()
            return
        if self.main_frame != 1:
            self.main_frame.destroy()
        self.main_frame = tkinter.Frame(self.root, bg="#8b98a7")
        self.main_frame.pack(anchor=tkinter.CENTER, fill=tkinter.BOTH)
        self.the_frame = tkinter.Frame(self.main_frame, bg="#8b98a7")
        self.the_frame.pack(padx=50, pady=25)

        rowslist = [0, 0, 2, 4, 6, 2, 4, 6, ]
        columnlist = [0, 3, 0, 0, 0, 3, 3, 3, ]
        for type, row, column in zip(self.type, rowslist, columnlist):
            self.light_label = tkinter.Label(self.the_frame, text=type, bg="#8b98a7", fg="#222222",
                                             font=("微软雅黑", 11)).grid(row=row,
                                                                     column=column)
        ph_tuple = ("all", "4-5", "5-6", "6-7", "7-8", "8-9", "9-10")
        self.ph_combobox = tkinter.ttk.Combobox(self.the_frame, values=ph_tuple, width=11, font=("微软雅黑", 10))
        self.ph_combobox.current(0)
        self.ph_combobox.bind("<<ComboboxSelected>>", self.handle_ph_combobox)
        self.ph_combobox.grid(row=0, column=1, pady=10)
        self.light_combobox = tkinter.ttk.Combobox(self.the_frame, values=self.light_tuple_all, width=14,
                                                   font=("微软雅黑", 10))
        self.light_combobox.current(0)
        self.light_combobox.bind("<<ComboboxSelected>>", self.handle_light_combobox)
        self.light_combobox.grid(row=0, column=4, pady=10)
        # Entry
        self.temp = tkinter.StringVar()
        self.temp.set("°c")
        self.rh = tkinter.StringVar()
        self.rh.set("%rh")
        self.sm = tkinter.StringVar()
        self.sm.set("S/m")
        self.n = tkinter.StringVar()
        self.n.set("mg/kg")
        self.p = tkinter.StringVar()
        self.p.set("mg/kg")
        self.k = tkinter.StringVar()
        self.k.set("mg/kg")

        # for代替失败，原因是bind函数效果不理想
        # rowlist = [2,4,6,2,4,6]
        # columnlist = [1,1,1,4,4,4]
        # for unit,row,column in zip(self.units[2:8],rowlist,columnlist):
        #     self.content = tkinter.StringVar()
        #     self.content.set(unit)
        #     self.entry = tkinter.Entry(self.the_frame, width=10, textvariable=self.content)
        #     self.entry.grid(row=row,column=column)
        #     self.entry.bind(sequence="<Button-1><ButtonRelease-1>", func=self.delete_test_text)
        self.rh_entry = tkinter.Entry(self.the_frame, width=10, textvariable=self.rh, font=("微软雅黑", 10))
        self.sm_entry = tkinter.Entry(self.the_frame, width=10, textvariable=self.sm, font=("微软雅黑", 11))
        self.temp_entry = tkinter.Entry(self.the_frame, width=10, textvariable=self.temp, font=("微软雅黑", 11))
        self.n_entry = tkinter.Entry(self.the_frame, width=10, textvariable=self.n, font=("微软雅黑", 11))
        self.p_entry = tkinter.Entry(self.the_frame, width=10, textvariable=self.p, font=("微软雅黑", 11))
        self.k_entry = tkinter.Entry(self.the_frame, width=10, textvariable=self.k, font=("微软雅黑", 11))
        self.rh_entry.bind(sequence="<Button-1><ButtonRelease-1>", func=self.choose_rh_text)
        self.sm_entry.bind(sequence="<Button-1><ButtonRelease-1>", func=self.choose_sm_text)
        self.temp_entry.bind(sequence="<Button-1><ButtonRelease-1>", func=self.choose_temp_text)
        self.n_entry.bind(sequence="<Button-1><ButtonRelease-1>", func=self.choose_n_text)
        self.p_entry.bind(sequence="<Button-1><ButtonRelease-1>", func=self.choose_p_text)
        self.k_entry.bind(sequence="<Button-1><ButtonRelease-1>", func=self.choose_k_text)
        self.temp_entry.grid(row=2, column=1, pady=20)
        self.rh_entry.grid(row=4, column=1, pady=20)
        self.sm_entry.grid(row=6, column=1, pady=20)
        self.n_entry.grid(row=2, column=4, pady=20)
        self.p_entry.grid(row=4, column=4, pady=20)
        self.k_entry.grid(row=6, column=4, pady=20)
        # 查询
        self.submit_search_button = tkinter.Button(self.the_frame, text="查询所有植物 ", font=("微软雅黑", 12), bg="#8b98a7",
                                                   fg="#222222", width=20)
        self.search_or_sub = "search"
        self.submit_search_button.bind("<Button-1>", self.check_search_key)
        self.submit_search_button.grid(row=9, column=1, columnspan=5, pady=20)

    # 反向搜索使用
    def handle_ph_combobox(self, event):
        self.ph_Var.set(self.ph_combobox.get())
    def handle_light_combobox(self, event):
        self.light_Var.set(self.light_combobox.get())

    # 王八蛋东西，循环失败，只能一个个写
    def choose_rh_text(self, event):
        self.rh_entry.selection_range(0, tkinter.END)
    def choose_temp_text(self, event):
        self.temp_entry.selection_range(0, tkinter.END)
    def choose_sm_text(self, event):
        self.sm_entry.selection_range(0, tkinter.END)
    def choose_n_text(self, event):
        self.n_entry.selection_range(0, tkinter.END)
    def choose_p_text(self, event):
        self.p_entry.selection_range(0, tkinter.END)
    def choose_k_text(self, event):
        self.k_entry.selection_range(0, tkinter.END)
    def choose_nickname_text(self, event):
        self.nickname_entry.selection_range(0, tkinter.END)
    def choose_pw_text(self, event):
        self.pwentry.selection_range(0, tkinter.END)
    def choose_account_text(self, event):
        self.account_entry.selection_range(0, tkinter.END)
    def delete_pw_text(self):
        self.pwentry.delete(0, tkinter.END)
    def delete_account_text(self):
        self.pwentry.delete(0, tkinter.END)
    def delete_r_account_text(self, event):
        self.account_r_entry.selection_range(0, tkinter.END)
    # 单击删除plant_entry中的默认内容：请输入植物名
    def delete_plant_text(self, event):
        self.plant_entry.selection_range(0, tkinter.END)

    # 修改昵称
    def set_nickname(self):
        if self.menu_in == False:
            self.out_of_menu()
            return
        self.sql_judge = 4
        if self.main_frame != 1:
            self.main_frame.destroy()
        self.nickname = tkinter.StringVar()
        self.nickname.set(self.username.get())
        self.main_frame = tkinter.Frame(self.root, bg="#8b98a7")
        self.main_frame.pack(anchor=tkinter.CENTER, pady=120)

        self.nickname_entry = tkinter.Entry(self.main_frame, width=20, font=("微软雅黑", 12,), bg="#dddddd",
                                            highlightcolor="#0000ff", textvariable=self.nickname)
        self.nickname_entry.bind(sequence="<Button-1><ButtonRelease-1>", func=self.choose_nickname_text)
        self.nickname_entry.bind("<Return>", self.sql_split)
        self.nickname_entry.grid(row=1, )

        self.submit_nickname_button = tkinter.Button(self.main_frame, font=("微软雅黑", 12), text="修改昵称", fg="#333333",
                                                     bg="#8b98a7",
                                                     command=self.sql_split_without_event)
        self.submit_nickname_button.grid(row=4, pady=30)

    # 展示昵称
    def show_nickname(self):
        # 在SQL中获取nickname
        try:
            name = pro_sql.nicknamesql(self.username.get())
        except Exception as e:
            '''
            # 这个是输出错误类别的，如果捕捉的是通用错误，其实这个看不出来什么
            print('str(Exception):\t', str(Exception))  # 输出  str(Exception):	<type 'exceptions.Exception'>
            # 这个是输出错误的具体原因，这步可以不用加str，输出
            print('str(e):\t\t', str(e))  # 输出 str(e):		integer division or modulo by zero
            print('repr(e):\t', repr(e))  # 输出 repr(e):	ZeroDivisionError('integer division or modulo by zero',)
            print('traceback.print_exc():')
            # 以下两步都是输出错误的具体位置的
            traceback.print_exc()  # 红色提示       
            '''
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            # tkinter.messagebox.showinfo("提示", "网络繁忙 或 昵称过长")
        else:  # 没发生异常
            self.nickname.set(name)
        self.nickname_plus = tkinter.StringVar()
        self.nickname_plus.set("尊敬的用户 " + self.nickname.get() + " 您好!")
        self.main_label.destroy()
        if hasattr(self, 'nickname_label'):
            self.nickname_label.destroy()
        self.nickname_label = tkinter.Label(self.root, textvariable=self.nickname_plus, bg="#8b98a7", fg="#222222",
                                            font=("微软雅黑", 10))
        self.nickname_label.pack(anchor=tkinter.NW, side=tkinter.TOP)

    # 右键显示位置
    def popup_handle(self, event):  # 处理菜单按钮
        self.pop_menu.post(event.x_root, event.y_root)

    # 设置
    def tip(self):
        tkinter.messagebox.showinfo("⚠️虚晃一枪", "⚠ 没啥好设置的")


if __name__ == '__main__':
    Window()
