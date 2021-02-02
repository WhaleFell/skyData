'''
Author: WhaleFall
Date: 2021-02-01 10:57:20
LastEditTime: 2021-02-02 11:33:36
Description: sky光遇官网爬虫
Url:https://game.163.com/star/sky/index.html 光遇博物馆
'''
import requests
import csv
import codecs  # 处理csv乱码
import re
import time  # 处理时间
import sys # 获取脚本目录

path=sys.path[0]

# 获取当前时间 2021-01-23
new_time = time.strftime("%Y-%m-%d")

# print(new_time)


# 获取 传入获取页数 60 120 180这样递增 但是每次只返回60条数据
def getContent(page):
    url = "https://kol.tongren.163.com/article/"
    data = {
        "sort": "new",
        "game": "光遇",
        "random_hot_value": "10",
        "span": "60",  # 每次获取的条数
        "start": str(page),
    }
    header = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
        "Host": "kol.tongren.163.com",
        "Origin": "http://game.163.com",
        "Referer": "http://game.163.com/star/sky/index.html",
    }

    try:
        response = requests.get(url, data=data, headers=header).json()
        # print(response)
        articles = response["data"]["articles"]
        if articles==[]:
            print("全部采集完毕!")
            return "全部采集完毕!"
    except Exception as e:
        print("[Eroor]响应信息:", response)
        raise

    DataAll = []  #所有数据
    # 取一个用户的主体数据
    for arts in articles:
        # print(arts)
        name = arts["author"]["nickname"]  # 作者名字

        # 遍历取用户主体数据
        datas = arts['body']  # 用户主体数据里面的主体内容
        picList = []  #储存图片链接
        for data in datas:

            content = data.get('fp_data')
            if content == None:
                text_content = data.get('text_content')
            else:
                text_content = None
                pic_url = content.get("url")
                picList.append(pic_url)  # 添加到图片列表

        tags = arts['tags'][0]  # 标签
        title = arts['title']  # 标题
        times = arts["publish_time"]  #时间
        # print(times)
        # 正则写的好菜 处理时间 处理后:2021-01-23 12:53:43
        pat = re.compile(r"(.*?)T\d\d:\d\d:\d\d")
        pat_check = re.compile(r"(.*?)T")

        time_s = pat.search(times).group().replace("T", " ")

        times_check = pat_check.findall(times)[0]
        # print(times_check)

        # 判断日期
        # if times_check != new_time:
        #     print(times_check,new_time)
        #     return "stop"
        # print(title, tags, name, picList, times)

        dictData = {
            "title": title,
            "text": text_content,
            "tags": tags,
            "name": name,
            "picList": picList,
            "time": time_s
        }
        # print(dictData)
        DataAll.append(dictData)

    # print(DataAll)
    return DataAll


# getContent(999999)

page = 0
# 初始化csv
with codecs.open("{}//skyDate {}.csv".format(path,new_time), "w", encoding="utf_8_sig") as cvs_file:

    headers = ["title", "text", "tags", "name", "picList", "time"]  #表头
    writer = csv.DictWriter(cvs_file, headers)
    writer.writeheader()  #写表头

while True:
    print("[suc]获取第{}条数据".format(page))
    Data = getContent(page)  #字典数据
    # if Data == "stop":
    #     print("[stop]获取到指定日期停止")
    #     break
    with codecs.open("{}//skyDate {}.csv".format(path,new_time), "a", encoding="utf_8_sig") as cvs_file:
        writer = csv.DictWriter(cvs_file, headers)
        writer.writerows(Data)  #写入多行
    page = page + 60
