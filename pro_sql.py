# Author:  @ MuLun_Zhu
# @Time :  2020/2/15 10:03 上午
# 提交text

import pymysql

# 工作目录
db = pymysql.connect(host="124.71.184.35", user="root", password="Czr8686478//", database="plant", port=3306)
cur = db.cursor()


# 注册sql验证
def registersql(id, pwd):
    register_sql = "insert into user(iduser,password) values(%d,'%s');" % (int(id), pwd)
    print(register_sql)
    cur.execute(register_sql)
    db.commit()
    num1 = cur.rowcount
    print(num1)
    if num1 != 1:
        print("注册 失败失败失败")
        return False
    else:
        print("注册 成功成功成功")
        return True


# 登录sql验证
def signsql(iduser, pwd):
    sign_sql = "select user.iduser,user.password from user where iduser=%d and password='%s';" % (int(iduser), pwd)
    print(sign_sql)
    cur.execute(sign_sql)
    longth = cur.fetchall()
    print(longth)
    if len(longth) != 1:
        print("登录 sql注入")
        return "warn"
    else:
        print("登录 成功成功成功")
        return "ok"


# 判断账号是否存在 登录界面
def sign_sql_account_exist(iduser):
    sign_sql = "select user.iduser,user.password from user where iduser=%d ;" % (int(iduser))
    print(sign_sql)
    cur.execute(sign_sql)
    longth = cur.fetchall()
    print(longth)
    print(len(longth))
    if len(longth) == 0:
        print("登录失败 账号不存在")
        return "no"
    elif len(longth) == 1:
        print("登录 存在此账号")
        return "yes"
    else:
        print("sql注入")
        return "no"


# 登陆后自动显示昵称
def nicknamesql(name):
    # try:
    sign_sql = "select user.nickname from user where iduser=%s;"
    print(sign_sql)
    cur.execute(sign_sql, (name))
    # except Exception as result:
    #     print(result)
    # else:
    longth = cur.fetchall()
    print(longth)
    nickname_str = longth[0][0]
    print(nickname_str)
    if isinstance(nickname_str, str):
        print("昵称获取成功")
        return nickname_str
    else:
        print("昵称获取失败")
        return False


# 密码更新
def pwdsql(id, pwd):
    register_sql = "update user set password='%s' where iduser=%d;" % (pwd, int(id))
    print(register_sql)
    cur.execute(register_sql)
    db.commit()
    num2 = cur.rowcount
    if num2 != 1:
        print("更新密码 失败失败失败")
        return 0
    else:
        print("更新密码 成功成功成功")
        return 1


# 更改昵称
def nickname_change_sql(name, nickname):
    register_sql = "update user set nickname=%s where iduser=%s;"
    print(register_sql)
    cur.execute(register_sql, (nickname, name))
    db.commit()
    num3 = cur.rowcount
    if cur.rowcount != 1:
        print("更改昵称 失败失败失败")
        return 0
    else:
        print("更改昵称 成功成功成功")
        return 1


# 输入植物名，搜索环境
def search_for_environment(name):
    register_sql = "select info.name,info.type,info.ph,info.light,info.temp,info.rh,info.sm,info.n,info.p,info.k from info where name like '%{name}%';".format(
        name=name)
    print(register_sql)
    cur.execute(register_sql)
    tuple_info = cur.fetchall()
    print("serach_tuple_info = ", end="")
    print(tuple_info)
    num4 = len(tuple_info)
    print(num4)
    # tuple处理成列表
    list_info = []
    for tuple in tuple_info:
        midden = []
        for item in tuple:
            midden.append(item)
        list_info.append(midden)

    if num4 == 0:
        print("无相关数据 ")
        return 0
    elif num4 >= 2:
        print("多条数据，默认使用第一条")
        return list_info
    else:
        print("一条数据 成功成功成功")
        return list_info


# 筛选正向检索结果
def filtrate(name, type):
    filtrate_sql = "select info.name,info.type,info.ph,info.light,info.temp,info.rh,info.sm,info.n,info.p,info.k from info where name like '%{name}%' and type like '%{type}%';".format(
        name=name, type=type)
    print(filtrate_sql)
    cur.execute(filtrate_sql)
    tuple_info = cur.fetchall()
    print("filtrate_tuple_info = ", end="")
    print(tuple_info)
    num4 = len(tuple_info)
    print(num4)
    # tuple处理成列表
    list_info = []
    for tuple in tuple_info:
        midden = []
        for item in tuple:
            midden.append(item)
        list_info.append(midden)

    if num4 == 0:
        print("无相关数据 ")
        return 0
    else:
        return list_info


# 根据环境，搜索植物
def search_for_plant_sql(info_list):
    if info_list[0] == "4-5":
        info_list[0] = "4%"
    elif info_list[0] == "5-6":
        info_list[0] = "5%"
    elif info_list[0] == "6-7":
        info_list[0] = "6%"
    elif info_list[0] == "7-8":
        info_list[0] = "7%"
    elif info_list[0] == "8-9":
        info_list[0] = "8%"
    elif info_list[0] == "9-10":
        info_list[0] = "9%"

    change_list = [5, 5, 5, 5, 5, 5]
    for index, item in enumerate(info_list[2:]):
        if item == 5000:
            change_list[index] = 5000
    print(change_list)

    filtrate_sql = "select info.name,info.type,info.ph,info.light,info.temp,info.rh,info.sm,info.n,info.p,info.k" \
                   " from info where" \
                   " info.ph like '%s' and" \
                   " info.light like '%s' and" \
                   " info.temp between %d and %d and" \
                   " info.rh between %d and %d and" \
                   " info.sm between %d and %d and" \
                   " info.n between %d and %d and" \
                   " info.p between %d and %d and" \
                   " info.k between %d and %d;" % (info_list[0], info_list[1],
                                                   info_list[2] - change_list[0], info_list[2] + change_list[0],
                                                   info_list[3] - change_list[1], info_list[3] + change_list[1],
                                                   info_list[4] - change_list[2], info_list[4] + change_list[2],
                                                   info_list[5] - change_list[3], info_list[5] + change_list[3],
                                                   info_list[6] - change_list[4], info_list[6] + change_list[4],
                                                   info_list[7] - change_list[5], info_list[7] + change_list[5])
    print(filtrate_sql)
    cur.execute(filtrate_sql)
    info_tuple = cur.fetchall()
    print("for_plant_tuple_info = ", end="")
    print(info_tuple)
    num5 = len(info_tuple)
    print(num5)
    # tuple处理成列表
    list_info = []
    for tuple in info_tuple:
        midden = []
        for item in tuple:
            midden.append(item)
        list_info.append(midden)

    if num5 == 0:
        print("无相关数据 ")
        return 0
    else:
        return list_info


# 筛选反向检索结果
def filtrate_for_plant_sql(info_list, type):
    if info_list[0] == "4-5":
        info_list[0] = "4%"
    elif info_list[0] == "5-6":
        info_list[0] = "5%"
    elif info_list[0] == "6-7":
        info_list[0] = "6%"
    elif info_list[0] == "7-8":
        info_list[0] = "7%"
    elif info_list[0] == "8-9":
        info_list[0] = "8%"
    elif info_list[0] == "9-10":
        info_list[0] = "9%"

    change_list = [5, 5, 5, 5, 5, 5]
    for index, item in enumerate(info_list[2:]):
        if item == 5000:
            change_list[index] = 5000
    print(change_list)
    print(type)
    filtrate_sql = "select info.name,info.type,info.ph,info.light,info.temp,info.rh,info.sm,info.n,info.p,info.k" \
                   " from info where" \
                   " info.ph like '%s' and" \
                   " info.light like '%s' and " \
                   " info.type='%s'and " \
                   " info.temp between %d and %d and" \
                   " info.rh between %d and %d and" \
                   " info.sm between %d and %d and" \
                   " info.n between %d and %d and" \
                   " info.p between %d and %d and" \
                   " info.k between %d and %d;" % (info_list[0], info_list[1], type,
                                                   info_list[2] - change_list[0], info_list[2] + change_list[0],
                                                   info_list[3] - change_list[1], info_list[3] + change_list[1],
                                                   info_list[4] - change_list[2], info_list[4] + change_list[2],
                                                   info_list[5] - change_list[3], info_list[5] + change_list[3],
                                                   info_list[6] - change_list[4], info_list[6] + change_list[4],
                                                   info_list[7] - change_list[5], info_list[7] + change_list[5],)
    print(filtrate_sql)
    cur.execute(filtrate_sql)
    info_tuple = cur.fetchall()
    print("for_plant_tuple_info = ", end="")
    print(info_tuple)
    num5 = len(info_tuple)
    print(num5)
    # tuple处理成列表
    list_info = []
    for tuple in info_tuple:
        midden = []
        for item in tuple:
            midden.append(item)
        list_info.append(midden)

    if num5 == 0:
        print("无相关数据 ")
        return 0
    else:
        return list_info


# 提交数据
def submit_info(infolist):
    sub_sql = "insert into info (info.name,info.type,info.ph,info.light,info.temp,info.rh,info.sm,info.n,info.p,info.k)" \
              "values('{name}','{type}','{ph}','{light}',{temp},{rh},{sm},{n},{p},{k});".format(
        name=infolist[0], type=infolist[1], ph=infolist[3], light=infolist[2], temp=infolist[4], rh=infolist[5],
        sm=infolist[6], n=infolist[7], p=infolist[8], k=infolist[9])
    print(sub_sql)
    cur.execute(sub_sql)
    num6 = cur.rowcount
    db.commit()
    if num6 == 1:
        print("插入数据成功 ")
        return 1
    else:
        print("插入数据失败 ")
        return 0


# 关闭db和游标
def close_db_and_cur():
    cur.close()
    db.close()
    print("合法退出程序")
