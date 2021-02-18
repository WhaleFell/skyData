#!/bin/bash
source /etc/profile
path_shell=$(dirname $(readlink -f "$0"))
echo "脚本目录:"$path_shell""

cd $path_shell
# ./sky.py

if [ "$?" != "0" ];then
    echo "运行 sky.py 出现错误!"
    exit 1
fi

git add .
time=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "${time} 自动更新提交Sky_CSV文件"
git push -u github master
if [ "$?" != "0" ];then
    echo "推送到GitHub出现错误!"
    exit 1
fi







