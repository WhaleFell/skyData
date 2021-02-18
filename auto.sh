#!/bin/bash
source /etc/profile
path_shell=$(dirname $(readlink -f "$0"))
echo "脚本目录:"$path_shell""

cd $path_shell
python3 sky.py

if [ "$?" != "0" ];then
    echo "运行 sky.py 出现错误!"
    exit 1
fi

echo "##########初始化Git远程仓库#############"
git config --global user.name "adminwhalefall"
git config --global user.email "2734184475@qq.com"
git remote rm github
git remote add github git@github.com:adminwhalefall/skydata.git
echo "##########提交GitHub#############"
git add .
time=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "${time} 自动更新提交Sky_CSV文件"
git push -u github master
if [ "$?" != "0" ];then
    echo "推送到GitHub出现错误!"
    exit 1
fi







