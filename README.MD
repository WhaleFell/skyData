<!--
 * @Author: WhaleFall
 * @Date: 2021-02-02 10:58:16
 * @LastEditTime: 2021-02-02 14:05:12
 * @Description: 自述文件
-->
# 光遇官网——光遇博物馆爬虫脚本
## 前言
![献祭完的图片](https://i.loli.net/2021/02/02/lsPKiMowSvn94Ic.jpg)
![禁阁终点](https://i.loli.net/2021/02/02/qRJpxn52VYBuAKf.png)
> 感恩季 追光季 归属季 凛冬季 魔法季 圣岛季 预言季 很荣幸能陪光遇走到现在，还有那些温柔的人 这一年多 有笑 有泪 不管怎样，我永远不会忘记我在这里度过的时光，开完好友树的，只开了对话的，只加了好友的，甚至是点亮过的小黑，很高兴认识你们，这一路承蒙照顾 真的很爱光遇,祝光遇越来越好，陈老师加油!
## 介绍
- 1. **爬取页面--光遇博物馆**
  > https://game.163.com/star/sky/index.html
- 2. 在脚本目录生成 **skyData {time}.csv** 文件
  - 文件的结构:
    ```csv
    title,text,tags,name,picList,time
    标题,文字内容(一些没有),标签,作者名,图片列表,发表时间
    ```
- 3. 本脚本**可以一直爬取到`2019/6/27  2:06:24`的第一条内容**,标题好像是:
  > 与温暖的灵魂相遇
- 4. 在我的win10上用Excel读取CSV文件已**不存在中文乱码的问题**
  - 关于Python CSV中文乱码问题的解决:
  ```python
  import csv
  import codecs  # 处理csv乱码
  with codecs.open("XXX.csv".format(new_time), "w", encoding="utf_8_sig") as cvs_file:
        writer = csv.DictWriter(cvs_file, headers)
        writer.writeheader()  #写表头v
        writer.writerows(Data)  #写入多行字典数据
  ```
    >### 如果还是存在中文乱码问题的话请提交`issues`
## 运行
1. 一定要在 `python3.X` 环境下运行本项目
2. 运行前请安装requests模块:
   `pip3 install requests`
3. Linux运行:`sudo python3 sky.py`
## TODO
- [ ] 添加`crantab`自动运行和自动提交`Git`的`shell`**脚本**每天自动更新提交到`GitHub`
- [ ] 添加**下载列表中的图片功能**,并把图片按文件夹**归类**
- [ ] 爬取更多有关`Sky·光遇`的东西
## 后
- 此项目由一个**初中生**开发,仅供**学习用途**
- 如果有什么好的建议也欢迎提出**Issues**,也欢迎各位大佬**Pull resquests**这个项目.
- 诶呀! 点个**Star** 再走叭!! mua~ /可爱

