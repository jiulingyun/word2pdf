使用libreoffice+python实现的高效word转pdf项目，转换后的pdf容错率很低

## 安装libreoffice
我这里以CentOS8为例，安装命令如下：
```shell
dnf install libreoffice
```
## 安装python3
我这里以CentOS8为例，安装命令如下：
```shell
dnf install python3
```
## 一键安装脚本
```shell
bash <(curl -Ls https://gitee.com/hugo-yang/word2pdf/master/install.sh)
```
## 使用方法
启动服务
```shell
systemctl start word2pdf
```
停止服务
```shell
systemctl stop word2pdf
```
设置开机自启动
```shell
systemctl enable word2pdf
```
禁用开机自启
```shell
systemctl disable word2pdf
```
