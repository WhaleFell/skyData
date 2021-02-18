'''
Author: whalefall
Date: 2021-02-03 12:12:36
LastEditors: Please set LastEditors
LastEditTime: 2021-02-18 14:33:14
Description: 读取生成的CVS文件 最好是多线程下载里边的图片 并自动归类到一个文件夹里边
'''
import codecs
import csv
import os
import random
import string
import threading
import time
from ast import literal_eval
import re

import requests
from fake_useragent import UserAgent

# 创建数据下载文件夹
try:
    # os.mkdir("D://skyDownload")
    dirList = ["txt", "pic", "video"]  # 需要创建的下级目录
    for d in dirList:
        # 嵌套一个try防止有些憨憨手残删掉了一个文件夹导致新建失误
        try:
            os.makedirs("D://skyDownload//{}".format(d))
        except FileExistsError:
            continue
# except FileExistsError:
#     print("文件夹已存在!")
except Exception as e:
    # 通常是权限之类的错误叭
    print("创建文件夹时出现未知错误", e)

# 生成随机数


def ran():
    charlist = [random.choice(string.ascii_uppercase) for i in range(6)]
    chars = ''.join(charlist)
    return chars

# 去除不合规则的文件名


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

# 下载保存函数 传入:类型(pic,txt,video) 作者 标题 标签 链接(文字) 没有的传0即可


def download(contentType, name, title, tags, url):
    if contentType == "txt":
        name = validateTitle(name)
        title = validateTitle(title)

        with open(r"D://skyDownload//txt//{}_{}.txt".format(title, name), "w",encoding="utf8") as txt:
            txt.write(str(url))
            print("[Txt]../txt/{}_{}.txt 下载成功".format(title, name))

    elif contentType == "pic":  # 这里要新建标签文件夹 如果存在异常处理直接写入

        resp = requests.get(
            url, headers={"User-Agent": UserAgent().random}).content

        try:
            os.makedirs(r"D://skyDownload//pic//{}".format(tags))
            time_s = ran()
            with open(r"D://skyDownload//pic//{}//{}.jpg".format(tags, time_s), "wb") as pic:
                pic.write(resp)
                print("[Pic]../pic/{}/{}.jpg 下载成功".format(tags, time_s))
        except FileExistsError:  # 文件夹已存在时 直接由时间戳命名算了 随机字母
            time_s = ran()
            with open(r"D://skyDownload//pic//{}//{}.jpg".format(tags, time_s), "wb") as pic:
                pic.write(resp)
                print("[Pic]../pic/{}/{}.jpg 下载成功".format(tags, time_s))
        except Exception as e:
            print("下载图片出现错误!", e)

    elif contentType == "video":
        resp = requests.get(
            url, headers={"User-Agent": UserAgent().random}).content

        title = validateTitle(title)
        with open("D://skyDownload//video//{}.mp4".format(title), "wb") as video:
            video.write(resp)
            print("[Video]../Video/{}.mp4 下载成功".format(title))
    else:
        raise TypeError("传入的类型参数错误!")


# download("txt", "hyy", "sas", "sa", "http://baidu.com")

# 列出脚本目录下的文件 并匹配csv文件
result = os.listdir(os.getcwd())

for csvFileName in result:
    if ".csv" in csvFileName:
        # 匹配到一个就退出了
        csv_path = "{}\{}".format(os.getcwd(), csvFileName)
        print("在脚本目录找到的.CSV文件:{}".format(csv_path))
        break

with codecs.open("{}".format(csv_path), "r", encoding="utf_8_sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        tags = row["tags"]
        text = row["text"]
        picList = literal_eval(row["picList"])
        # print(picList)
        name = row["name"]
        title = row["title"]
        # 这里可能会出现诡异错误
        try:
            # print(tags,text,picList,name,title)
            # - 判断文字为空的情况
        # 为空-->判断tags是否为视频
        #       -->否 下载图片到 ../pic/图片标签文件夹/.jpg
        #       -->是 下载视频到 ../video/视频标题.mp4
        # - 不为空-->把文字下载到 ../txt/标题——作者.txt

            if text == "":
                if tags == "视频":
                    if picList == "[]":
                        pass
                    for url in picList:
                        download("video", name, title, tags, url)
                else:
                    if picList == "[]":
                        pass
                    for url in picList:
                        # print(url)
                        download("pic", name, title, tags, url)
            else:
                download("txt", name, title, tags, text)

        except ConnectionResetError:

            print("爬取太快!服务器可能拒绝!")
            time.sleep(10)

        except Exception as e:
            print("出现诡异错误",e)
            time.sleep(4)
        finally:
            continue
