'''
Author: whalefall
Date: 2021-02-17 06:56:41
LastEditTime: 2021-02-18 18:51:11
Description: Sky光遇随机图api
'''
import csv
from flask import *
import json
import os
import sys
import pandas as pd
import random
from ast import literal_eval  # 将字符串列表转化为列表

# 功能函数部分
# 获取目录下的第一个CSV文件


def getCsvPath():
    result = os.listdir(os.getcwd())

    for csvFileName in result:
        if ".csv" in csvFileName:
            csv_path = os.path.join(os.getcwd(), csvFileName)
            return csv_path
        else:
            pass

    print("[Error]目录下无法找到CSV文件!即将调用 sky.py 生成")
    os.system("python {}".format(os.path.join(os.getcwd(), "sky.py")))
    sys.exit()

# 读取CSV文件


def readCSV(path):
    df = pd.read_csv(path)
    # index_num = df.shape[0]  # 取出总行数
    index_num = len(df.index)
    rand = random.randint(1, index_num)
    # 取出的数据标签不能为视频 并 图片列表不为空！
    df = df[(df["tags"] != "视频") & (
        df["picList"] != "[]")]

    data = df.loc[rand:rand]  # 取出随机某一列

    # 取出数据
    title = data["title"].values[0]
    text = data["text"].values[0]
    tags = data["tags"].values[0]
    # Empty DataFrame
    pic_url = random.choice(literal_eval(data["picList"].values[0]))
    time = data["time"].values[0]

    return str(title), str(text), str(tags), str(pic_url), str(time)


# readCSV(getCsvPath())


# Flask接口部分
app = Flask(__name__)

# 返回json信息


@app.route("/sky/json/", methods=["GET", "POST"])
def skyJson():
    try:
        try:
            title, text, tags, pic_url, time = readCSV(getCsvPath())
        except IndexError:
            print("[Error]可能出现了Empty DataFrame错误 我也不知道怎么解决了唉 重新生成试试")
            title, text, tags, pic_url, time = readCSV(getCsvPath())

        if text == "NaN" or text == "nan":
            content = title + "|" + tags
        else:
            content = title + "|" + text

        dictData = {
            "status": 200,
            "data": {
                "title": title,
                "text": text,
                "tag": tags,
                "time": time,
                "pic_url": pic_url,
                "content": content,
            }
        }

    except IndexError:
        dictData = {
            "status": 500,
            "data": {
                "content": "出现了极低概率的错误(两次Empty DataFrame),请重新发送请求叭",
                "pic_url": "https://i.loli.net/2021/02/18/w36CqS2FPkdvcV9.jpg",
            }
        }
    except Exception as e:
        dictData = {
            "status": 500,
            "data": {
                "content": "出现了其他异常 %s" % (e),
                "pic_url": "https://i.loli.net/2021/02/18/w36CqS2FPkdvcV9.jpg",
            }
        }
    return json.dumps(dictData, ensure_ascii=False)

# 直接重定向到图片


@app.route("/sky/pic/", methods=["GET", "POST"])
def skyPic():
    try:
        try:
            title, text, tags, pic_url, time = readCSV(getCsvPath())
        except IndexError:
            print("[Error]可能出现了Empty DataFrame错误 我也不知道怎么解决了唉 重新生成试试")
            title, text, tags, pic_url, time = readCSV(getCsvPath())
    except Exception as e:
        print("[Error]出现其他异常%s" % e)
        return redirect("https://i.loli.net/2021/02/18/w36CqS2FPkdvcV9.jpg")
    else:
        return redirect(pic_url)


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
