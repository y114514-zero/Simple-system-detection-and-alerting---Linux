# 🚀介绍
Ansible 一键部署监控系统
本目录包含用于自动化部署 Simple System Monitor 全套监控环境的 Ansible 剧本和角色。通过执行一个命令，即可在目标主机上完成：
- **安装 Python 环境与项目依赖**
- **部署监控脚本并注册为 systemd 服务**
- **安装与配置 MySQL 数据库（可选）**
- **安装并配置 Prometheus 与 Grafana**
- **配置 Prometheus 抓取监控脚本的 /metrics 接口**

# 📁 目录结构
text
```
ansible/
├── inventory              # 主机清单（需自行编辑）
├── Playbook.yaml          # 主剧本，调用各个角色
├── README.md              # 本文件
└── roles/                 # Ansible 角色
    ├── install/           # 部署监控脚本（Python 依赖、systemd 服务）
    ├── mysql/             # 安装 MySQL，创建数据库与用户
    └── prometheus/        # 安装 Prometheus 与 Grafana，配置抓取
```

# 📦 前置条件
- **控制机**：已安装 Ansible。
- **目标主机**：Linux 系统（支持 CentOS 7+/8+、Ubuntu 18.04+ 等），可 SSH 登录，且具有 sudo 权限。
- **网络**：目标主机需能访问互联网以下载软件包。

# ⚙️ 配置说明
### 1. 编辑主机清单（inventory）
打开ansible目录下的inventory（主机清单）
```
[monitor_hosts]
your_ip ansible_user=your_user ansible_ssh_pass=your_password
```
若使用密钥登录可以将验证改为ansible_ssh_private_key_file=~/.ssh/id_rsa

### 2. 修改变量
```
##roles/install/var/main.yaml
# 项目的路径
path: "your_installtion_rootpath"

##roles/mysql/var/main.yaml
# 定义mysql的密码
mysql_password: "your_password"
# 项目的路径
path: "your_installtion_rootpath"

##roles/mysql/task/main.yaml
- name: 初始化数据库
  shell: "/export/server/mysql/bin/mysql < /{{path}}/Simple-system-detection-and-alerting---Linux/ansible/roles/mysql/files/init_db.sql -pyour_database_login_password"

##roles/prometheus/var/main.yaml
# 你要监控的主机
monitor_host: "localhost[default]"
path: "your_installtion_rootpath"

```

# ✅ 验证部署
部署完成后，可通过以下方式验证各组件是否正常运行：
- 监控脚本：systemctl status monitor，应显示 active (running)。
- Prometheus：访问 http://目标IP:9090，查看是否能看到 CPU_use_percent 等指标。
- Grafana：访问 http://目标IP:3000，默认用户名/密码为 admin/admin。
- MySQL：mysql -u monitor_user -p -e "SELECT * FROM system_monitor.metrics LIMIT 5;"，应能看到监控数据。

——————————————————————————————————————————————————————————————————————————————————————————————————————————————
# 🚀 introduction
Ansible one-click deployment monitoring system
This directory contains Ansible playbooks and roles for automating the deployment of the complete monitoring environment for Simple System Monitor. By executing a single command, you can complete the deployment on the target host:
- **Install Python environment and project dependencies**
- **Deploy the monitoring script and register it as a systemd service**
- **Installing and configuring MySQL database (optional)**
- **Install and configure Prometheus and Grafana**
- **Configure the /metrics interface for Prometheus to scrape monitoring scripts**
# 📁 Directory structure
text
```
ansible/
├─ inventory              # Host inventory (needs to be edited manually)
├─ Playbook.yaml          # Main playbook, calling various roles
├─ README.md              # This file
└── roles/                 # Ansible roles
    ├─ install/           # Deployment monitoring scripts (Python dependencies, systemd services)
    ├─ mysql/             # Install MySQL, create databases and users
    └── prometheus/        # Install Prometheus and Grafana, configure data scraping
```
# 📦 Preconditions
- **Control machine**: Ansible has been installed.
- **Target Host**: Linux system (supporting CentOS 7+/8+, Ubuntu 18.04+, etc.), SSH login enabled, and with sudo privileges.
- **Network**: The target host must be able to access the Internet to download software packages.
# ⚙️ Configuration instructions
### 1.  Edit the inventory of hosts
Open the inventory (host inventory) in the Ansible directory
```
[monitor_hosts]
your_ip ansible_user=your_user ansible_ssh_pass=your_password
```
If logging in with a key, you can change the authentication to `ansible_ssh_private_key_file=~/.ssh/id_rsa`
### 2.  Modify variables
```
##roles/install/var/main.yaml
# Path of the project
path: "your_installtion_rootpath"
##roles/mysql/var/main.yaml
# Define the password for MySQL
mysql_password: "your_password"
# Path of the project
path: "your_installtion_rootpath"
##roles/mysql/task/main.yaml
- name: Initialize Database
  shell: "/export/server/mysql/bin/mysql < /{{path}}/Simple-system-detection-and-alerting---Linux/ansible/roles/mysql/files/init_db.sql -pyour_database_login_password"
##roles/prometheus/var/main.yaml
# The host you want to monitor
monitor_host: "localhost[default]"
path: "your_installtion_rootpath"
```
# ✅ Verify deployment
After deployment is complete, you can verify whether each component is operating normally by the following methods:
- Monitoring script: systemctl status monitor should display "active (running)".
- Prometheus: Access http://target_IP:9090 to check if metrics such as CPU_use_percent are visible.
- Grafana: Access http://target_IP:3000, with default username/password as admin/admin.
- MySQL: mysql -u monitor_user -p -e "SELECT * FROM system_monitor.metrics LIMIT 5;"，You should be able to see the monitoring data.
