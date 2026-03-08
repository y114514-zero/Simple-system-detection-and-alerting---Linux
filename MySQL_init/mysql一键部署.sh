#!/bin/bash

echo "正在安装mysql......"
# 1.先下载lib软件
dnf -y install libaio
if [ $? -ne 0 ]; then
    echo "lib下载失败"
    exit 1
fi 

echo "lib包安装成功"

echo "正在创建mysql安装目录"
mkdir -p /export/server/

#2. 判断根目录是否有mysql压缩包,有就解压并重命名
if [ -f /root/mysql-8.0.40-linux-glibc2.28-x86_64.tar.xz ]; then
    echo "检测到有压缩包，执行解压操作..."
    tar -xvf /root/mysql-8.0.40-linux-glibc2.28-x86_64.tar.xz -C /export/server/
    cd /export/server/
    ls -l
    mv mysql-8.0.40-linux-glibc2.28-x86_64 mysql 
fi

echo "正在查询是否有mysql用户......"

#3. 判断是否有mysql用户，没有就创建
id mysql
if [ $? -ne 0 ]; then
    echo "没有这个用户，执行创建..."
    useradd -r -s /sbin/nologin mysql
    echo "用户创建成功"
fi

echo "正在查询是否有Mariadb包......"
#4. 查看是否有Mariadb包，有的话就删除，这里使用xargs
rpm -qa | grep mariadb | xargs -r dnf remove -y

#5. 删除原my.cnf文件
echo "正在查询是否有my.cnf文件......"
[ -f /etc/my.cnf ] && rm -rf /etc/my.cnf && echo "删除成功"

#7.可以初始化和添加ssl
echo "正在初始化与添加ssl......"
cd /export/server/mysql
bin/mysqld --initialize --user=mysql --datadir=/export/server/mysql/data --basedir=/export/server/mysql 2>&1 | tee /tmp/mysqld.log
grep password /tmp/mysqld.log | awk '{print $NF}' > /var/password.txt

echo "正在创建套接字"
bin/mysql_ssl_rsa_setup --datadir=/export/server/mysql/data

#8.创建服务项

echo "正在进行mysqld服务项创建....."
cat > /etc/systemd/system/mysqld.service <<EOF
[Unit]
Description=MySQL Server
After=network.target

[Service]
User=mysql
Group=mysql
Type=forking

# MySQL 执行命令及路径
ExecStart=/export/server/mysql/bin/mysqld --daemonize --pid-file=/export/server/mysql/data/mysqld.pid
ExecStop=/export/server/mysql/bin/mysqladmin --defaults-file=/export/server/mysql/my.cnf shutdown

# Ensure MySQL has sufficient time to start up
TimeoutSec=600

# PID 文件路径
PIDFile=/export/server/mysql/data/mysqld.pid

# Enable these options to auto-restart the service if it crashes
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

echo "服务项创建完成"

#9.创建my.cnf文件
echo "正在创建my.cnf......"
cat > /etc/my.cnf <<EOF
[mysqld]
port=3306
basedir=/export/server/mysql
datadir=/export/server/mysql/data
socket=/tmp/mysql.sock
character_set_server=utf8
collation-server=utf8_unicode_ci
EOF

echo "my.cnf文件创建成功"

#10.刷新服务项并启动查看状态

systemctl daemon-reload
systemctl start mysqld
systemctl enable mysqld
systemctl status mysqld &> /dev/null

echo "系统服务项添加完成"

#12.解决无法登录问题
[ ! -f /lib64/libncurses.so.5 ] && ln -s /lib64/libncurses.so.6 /lib64/libncurses.so.5
[ ! -f /lib64/libtinfo.so.5 ] && ln -s /lib64/libtinfo.so.6 /lib64/libtinfo.so.5

#11.重置密码为123456
pass=$(cat /var/password.txt)

bin/mysqladmin -uroot password '123456' -p$pass
echo "密码重置成功"

#6.添加全局变量
echo "export PATH=$PATH:/export/server/mysql/bin" >> /etc/profile
source /etc/profile

echo "全局变量添加成功"

#12.弹出提示
echo "mysql一键部署完成"
