red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
plain='\033[0m'

cur_dir=$(pwd)

[[ $EUID -ne 0 ]] && echo -e "${red}错误：${plain} 必须使用root用户运行此脚本！\n" && exit 1

install(){
    systemctl stop word2pdf
    cd /usr/local/
    last_version=$(curl -Ls "https://raw.githubusercontent.com/jiulingyun/word2pdf/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
    if [[ ! -n "$last_version" ]]; then
        echo -e "${red}检测 word2pdf 版本失败，可能是超出 Github API 限制，请稍后再试，或手动指定 word2pdf 版本安装${plain}"
        exit 1
    fi
    echo -e "检测到 word2pdf 最新版本：${last_version}，开始安装"
    wget -N --no-check-certificate -O /usr/local/word2pdf-${last_version}.tar.gz https://raw.githubusercontent.com/jiulingyun/word2pdf/releases/download/${last_version}/${last_version}.tar.gz
    if [[ $? -ne 0 ]]; then
        echo -e "${red}下载 word2pdf 失败，请确保你的服务器能够下载 Github 的文件${plain}"
        exit 1
    fi

    tar zxvf word2pdf-${last_version}.tar.gz
    rm word2pdf-${last_version}.tar.gz -f
    cd word2pdf-${last_version}

    # 将该目录下的word2pdf.service文件中的目录名word2pdf替换成变量word2pdf-${last_version}
    sed -i "s/word2pdf/word2pdf-${last_version}/g" word2pdf.service

    # 将该目录下的word2pdf.service文件复制到系统服务目录
    cp word2pdf.service /etc/systemd/system/word2pdf.service

    # 刷新服务缓存
    systemctl daemon-reload

    # 启动服务
    systemctl start word2pdf

    # 判断word2pdf服务是否启动成功
    if [[ $? -ne 0 ]]; then
        echo -e "${red}启动 word2pdf 服务失败，请检查是否安装成功${plain}"
        exit 1
    fi

    echo -e "${green}word2pdf 安装成功，已启动${plain}"
}

install
