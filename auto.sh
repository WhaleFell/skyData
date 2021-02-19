#!/bin/bash
# 酷推token
token="92f83d0596c7b553ea1df9f242e4fc46"
path_shell=$(dirname $(readlink -f "$0"))
echo "脚本目录:"$path_shell""

cd $path_shell
# python3 sky.py

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
# git_log=$(git push -u github master 2>&1)
cat /ectas/sasasa
if [ "$?" != "0" ];then
    content=""${time}"\n[skyData]推送到GitHub出现错误!\n"${git_log}""
    echo ${content}
    curl "https://push.xuthus.cc/send/"${token}"?c="${content}""
    exit 1
elif [ "$?" == "0" ];then
    content=""${time}"\n[skyData]推送到GitHub成功啦!\n"${git_log}""
    echo ${content}
    curl "https://push.xuthus.cc/send/"${token}"?c="${content}""
    exit 1
fi

# 强制同步远程仓库
# git fetch --all
# git reset --hard origin/master
# git fetch






