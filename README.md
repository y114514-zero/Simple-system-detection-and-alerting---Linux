# ✨ 核心功能
- **实时系统监控**：持续采集 CPU、内存、磁盘空间的使用率。
- **阈值告警**：可以通过配置文件自定义 CPU、内存、磁盘的告警阈值，超过阈值即会发送通知。
- **多指标采集**：监控磁盘读写速率（MB/s）与 I/O 次数，以及网络发送/接收速率（Mb/s）。
- **日志与数据持久化**：将关键指标写入本地日志文件和 MySQL 数据库，便于历史分析。
- **自动配置**：首次运行自动创建配置文件模板（.env 和 config.json），只需填写 Webhook 地址即可使用。
- **Prometheus** ：集成：通过 prometheus_client 暴露 /metrics 接口，可被 Prometheus 抓取，实现云原生监控。
- **跨平台支持**：基于 Python 和 psutil 库，可在 Linux、macOS、Windows 上运行。


# 🛠️ 技术栈
- 编程语言：Python 3.13+

- 核心依赖：

- `psutil`：用于采集系统资源信息。
- `requests`：用于发送 HTTP 告警请求。
- `python-dotenv`：用于管理环境变量配置文件。
- `pymysql`：用于实现python调用MySQL数据库参数。
- `prometheus-client`：Prometheus 指标暴露
- 配置格式：JSON (config.json) 与环境变量文件 (.env)


# ⭐️快速开始指南
## 1. 克隆仓库
bash

```properties
git clone https://github.com/y114514-zero/Simple-system-detection-and-alerting---Linux.git

cd Simple-system-detection-and-alerting---Linux
```

## 2. 安装依赖
推荐使用虚拟环境：

bash
创建虚拟环境（Python 3.6+）
python3 -m venv venv

激活虚拟环境
source venv/bin/activate   # Linux/Mac
或 .\venv\Scripts\activate  # Windows

然后安装依赖：

```properties
pip install -r requirements.txt
```
## 3. 安装MySQL并初始化（可选）
若没有，就执行（需要有MySQL软件包）MySQL一键部署脚本，并将init_db.sql初始化数据库导入到MySQL中
bash

```properties
source mysql一键部署.sh
systemctl start mysqld
systemctl enable mysqld
mysql < init_db.sql -pyourpassword
```

## 4. 配置
配置文件示例config.example.json：

bash

```properties
cp config.example.json config.json
```

然后根据需要编辑 config.json，修改阈值、日志路径等（默认值通常可直接使用）。

设置 Webhook URL：
直接运行脚本，它会自动检测并创建 .env 模板：

bash

```properties
python monitor.py
```

首次运行会提示：

text
❌ 未找到 .env 文件，已为你创建模板。请编辑 .env 填写正确的 URL 后重新运行脚本。
此时编辑生成的 .env 文件，填入你的企业微信/钉钉/飞书机器人 Webhook 地址：


text
url=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxx
## 5. 运行监控
再次运行脚本：

bash

```properties
python monitor.py
```

脚本会开始采集系统指标，并在终端实时显示。当 CPU、内存或磁盘使用率超过阈值时，会自动通过 Webhook 发送告警消息。


## 6. 后台运行（可选）
如果希望脚本在后台持续运行，可以使用以下方法：

使用 nohup：

bash

```properties
nohup python monitor.py > monitor.log 2>&1 &
```


## 7. 停止监控
如果是在前台运行，按 Ctrl+C 即可停止。

如果是后台运行，使用 ps aux | grep monitor.py 找到进程 ID 并 kill 它。

## 🚀 高级用法
使用 Ansible 一键部署
项目中包含 ansible/ 目录，可一键部署监控系统及其依赖（MySQL、Prometheus、Grafana）。详见 ansible/README.md。

对接 Prometheus
脚本启动后会监听 8000 端口，提供 /metrics 接口。在 Prometheus 配置中添加：

yaml
scrape_configs:
  - job_name: 'system_monitor'
    static_configs:
      - targets: ['localhost:8000']
之后在 Grafana 中导入 Prometheus 数据源，即可展示实时图表。
——————————————————————————————————————————————————
**更新日志**
[v1.20]
- 新增Prometheus 集成：引入 prometheus-client，通过 /metrics 端点暴露所有监控指标（CPU、内存、磁盘、网络 I/O），支持 Prometheus 原生抓取，实现云原生监控。
- 新增Grafana 可视化：提供预设仪表盘模板，可快速展示系统指标趋势，支持自定义图表与告警规则。
- 支持Ansible 一键部署：新增 ansible/ 目录，编写完整 Playbook 与 Roles，实现监控系统（脚本、MySQL、Prometheus、Grafana）的自动化部署，大幅降低配置门槛。
- 支持恢复通知：当 CPU/内存/磁盘使用率从超标状态恢复正常时，自动发送恢复消息，形成告警闭环。
- 支持数据库自动清理：MySQL 表中每插入 127 条记录后自动清空旧数据，防止表无限增长，保持查询性能。

[v1.10]
- 新增 MySQL 数据持久化功能，监控数据可存入数据库。
- 新增数据库初始化脚本 `init_db.sql`和`MySQL一键部署脚本`。
- 更新配置文件示例 `config.example.json`，增加 `mysql` 配置项。
- 修复磁盘 I/O 计算错误。

——————————————————————————————————————————————————

# ✨ Core Features
- **Real-time system monitoring**: Continuously collects usage rates of CPU, memory, and disk space.
- **Threshold Alerts**: The alert thresholds for CPU, memory, and disk can be customized through a configuration file. Notifications will be sent when the thresholds are exceeded.
- **Multi-metric collection**: Monitor disk read and write rates (MB/s) and I/O counts, as well as network send/receive rates (Mb/s).
- **Logging and data persistence**: Write key metrics to local log files and MySQL databases for historical analysis.
- **Automatic Configuration**: Upon first run, it automatically creates configuration file templates (both .env and config.json), requiring only the filling in of the Webhook address for use.
- **Prometheus**: Integration: The /metrics interface is exposed through prometheus_client, which can be scraped by Prometheus to achieve cloud-native monitoring.
- **Cross-platform support**: Based on Python and the psutil library, it can run on Linux, macOS, and Windows.
# 🛠️ Technology Stack
- Programming language: Python 3.13+
- Core dependencies:
- `psutil`: Used for collecting system resource information.
- `requests`: Used for sending HTTP alert requests.
- `python-dotenv`: Used for managing environment variable configuration files.
- `pymysql`: Used to implement the parameters for Python to call MySQL database.
- `prometheus-client`: Prometheus metric exposure
- Configuration format: JSON (config.json) and environment variable file (.env)
# ⭐️Quick Start Guide
## 1.  Clone repository
bash
```properties
git clone https://github.com/y114514-zero/Simple-system-detection-and-alerting---Linux.git
cd Simple-system-detection-and-alerting---Linux
```
## 2. Install dependencies
It is recommended to use a virtual environment:
bash
Create a virtual environment (Python 3.6+)
python3 -m venv venv
Activate virtual environment
source venv/bin/activate   # Linux/Mac
Or, run `.venv\Scripts\activate` # for Windows
Then install dependencies:
```properties
pip install -r requirements.txt
```
## 3.  Install MySQL and initialize it (optional)
If not, execute the MySQL one-click deployment script (requiring the MySQL software package), and import the init_db.sql initialization database into MySQL
bash
```properties
source mysql_one_click_deployment.sh
systemctl start mysqld
systemctl enable mysqld
mysql < init_db.sql -pyourpassword
```
## 4. configuration
Example configuration file: config.example.json:
bash
```properties
cp config.example.json config.json
```
Then, edit config.json as needed, modifying the threshold, log path, etc. (Default values can usually be used directly).
Set Webhook URL:
Run the script directly, and it will automatically detect and create an .env template:
bash
```properties
python monitor.py
```
The first run will prompt:
text
❌ The .env file was not found. A template has been created for you. Please edit the .env file, fill in the correct URL, and run the script again.
At this point, edit the generated .env file and fill in your Webhook address for the enterprise WeChat/DingTalk/Feishu robot:
text
url=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxx
## 5. operation monitoring
Run the script again:
bash
```properties
python monitor.py
```
The script will start collecting system metrics and displaying them in real-time on the terminal. When CPU, memory, or disk usage exceeds the threshold, an alert message will be automatically sent via Webhook.
## 6.  Background operation (optional)
If you want the script to run continuously in the background, you can use the following method:
Using nohup:
bash
```properties
nohup python monitor.py > monitor.log 2>&1 &
```
## 7.  Stop monitoring
If it is running at the foreground, you can press Ctrl+C to stop it.
If it's running in the background, use `ps aux | grep monitor.py` to find the process ID and kill it.
## 🚀 Advanced Usage
One-click deployment using Ansible
The project includes an ansible/ directory, which allows for one-click deployment of the monitoring system and its dependencies (MySQL, Prometheus, Grafana). For details, please refer to ansible/README.md.
Integrate with Prometheus
After the script is started, it will listen on port 8000 and provide the /metrics interface. Add the following to the Prometheus configuration:
yaml
scrape_configs:
  - job_name: 'system_monitor'
    static_configs:
      - targets: ['localhost:8000']
Afterwards, by importing the Prometheus data source into Grafana, real-time charts can be displayed.
——————————————————————————————————————————————————
**Update Log**
[v1.20]
- Added Prometheus integration: Introduced prometheus-client to expose all monitoring metrics (CPU, memory, disk, network I/O) through the /metrics endpoint, supporting native Prometheus scraping for cloud-native monitoring.
- Added Grafana visualization: Provides preset dashboard templates for quickly displaying system metric trends, and supports custom charts and alert rules.
- Support for Ansible one-click deployment: A new ansible/ directory has been added, with complete Playbooks and Roles written, enabling automated deployment of monitoring systems (scripts, MySQL, Prometheus, Grafana), significantly lowering the configuration threshold.
- Support for recovery notifications: When CPU/memory/disk usage returns to normal from an excessive state, a recovery message is automatically sent, forming a closed-loop alert system.
- Support for automatic database cleanup: After every 127 records are inserted into a MySQL table, the old data is automatically cleared to prevent the table from growing indefinitely and maintain query performance.
- 
[v1.10]
- Added MySQL data persistence function, allowing monitoring data to be stored in the database.
- Added database initialization script `init_db.sql` and `MySQL one-click deployment script`.
- Update the configuration file example `config.example.json` by adding the `mysql` configuration item.
- Fixed disk I/O calculation error.

