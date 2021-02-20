#!/bin/bash
path_shell=$(dirname $(readlink -f "$0"))
echo "脚本目录:"$path_shell""

cd $path_shell
py_log=$(python3 sky.py)
echo "###################获取完成####################"

if [ "$?" != "0" ];then
    echo "运行 sky.py 出现错误!"
    time=$(date "+%Y-%m-%d %H:%M:%S")
    python3 push.py "False" "${time}" "${py_log}"
    exit 1
fi

echo "##########初始化Git远程仓库#############"
git config --global user.name "adminwhalefall"
git config --global user.email "2734184475@qq.com"
git remote rm github
git remote add github git@github.com:AdminWhaleFall/skyData.git
echo "##########提交GitHub#############"
git add .
time=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "${time} 自动更新提交Sky_CSV文件"

t=0
while (( $t <= 10 ))
do
    git_log=$(git push -u github master 2>&1)
    # git_log=$(cat /sassass/sas 2>&1)
    if [ "$?" != "0" ];then
        echo "#############尝试第"$i"次##################"
        echo $git_log
        # exit 1
    else
        echo $git_log
        python3 push.py "True" "${time}" "${git_log}"
        exit 1
    fi
    let "t++"
done

python3 push.py "False" "${time}" "${git_log}"


# 强制同步远程仓库
# git fetch --all
# git reset --hard origin/master
# git fetch

# 请使用 /bin/bash 运行！这是一个极大的坑点





