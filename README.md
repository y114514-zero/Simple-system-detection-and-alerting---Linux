# ✨ 核心功能
- **实时系统监控**：持续采集 CPU、内存、磁盘空间的使用率。
- **阈值告警**：可以通过配置文件自定义 CPU、内存、磁盘的告警阈值，超过阈值即会发送通知。
- **多指标采集**：监控磁盘读写速率（MB/s）与 I/O 次数，以及网络发送/接收速率（Mb/s）。
- 日志记录：将关键指标自动写入本地日志文件，方便分析。

- 自动配置：首次运行自动创建配置文件模板（.env 和 config.json），用户只需填写 Webhook 地址即可使用。

- 跨平台支持：基于 Python 和 psutil 库，可在 Linux、macOS、Windows 系统上运行。


# 🛠️ 技术栈
- 编程语言：Python 3.13+

- 核心依赖：

- `psutil`：用于采集系统资源信息。
- `requests`：用于发送 HTTP 告警请求。
- `python-dotenv`：用于管理环境变量配置文件。
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

## 3. 配置
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
## 4. 运行监控
再次运行脚本：

bash

```properties
python monitor.py
```

脚本会开始采集系统指标，并在终端实时显示。当 CPU、内存或磁盘使用率超过阈值时，会自动通过 Webhook 发送告警消息。


## 5. 后台运行（可选）
如果希望脚本在后台持续运行，可以使用以下方法：

使用 nohup：

bash

```properties
nohup python monitor.py > monitor.log 2>&1 &
```


## 6. 停止监控
如果是在前台运行，按 Ctrl+C 即可停止。

如果是后台运行，使用 ps aux | grep monitor.py 找到进程 ID 并 kill 它。

——————————————————————————————————————————————————

# ✨ Key Functionality 
- Real-time system monitoring: Continuously collect the usage rates of CPU, memory, and disk space.
- Threshold alerts: Thresholds for CPU, memory, and disk can be customized through configuration files, and notifications will be sent when the thresholds are exceeded.
- Multi-indicator collection: Monitor disk read/write rates (MB/s) and I/O counts, as well as network sending/receiving rates (Mb/s).
- Log recording: Key indicators are automatically written to local log files for easy analysis.
- Automatic configuration: Automatically create configuration file templates (.env and config.json) on the first run. Users only need to fill in the Webhook address to use it.
- Cross-platform support: Based on Python and the psutil library, it can run on Linux, macOS, and Windows systems. 
# 🛠️ Technology Stack 
- Programming language: Python 3.13+
- Core dependencies:
- `psutil`: Used for collecting system resource information.
- `requests`: Used for sending HTTP alert requests.
- `python-dotenv`: Used for managing environment variable configuration files.
- Configuration format: JSON (config.json) and environment variable file (.env)



# ⭐️Quick Start Guide

## 1. Clone the repository bash
```properties
git clone https://github.com/y114514-zero/Simple-system-detection-and-alerting---Linux.git
cd Simple-system-detection-and-alerting---Linux
```

## 2. Installing Dependencies
It is recommended to use a virtual environment: 
bash
 Create a virtual environment (Python 3.6+ ) python3 -m venv venv
 Activate virtual environment source venv/bin/activate   # Linux/Mac
 Or. \venv\Scripts\activate  # Windows

Then install the dependencies: 
bash

```
pip install -r requirements.txt
```


## 3. Configuration
Configuration file example: config.example.json: 
bash

```properties
cp config.example.json config.json
```

Then, edit the config.json as needed, modifying the thresholds, log paths, etc. (the default values can usually be used directly). 
Set Webhook URL:
Simply run the script, and it will automatically detect and create the .env template: 
bash

```
python monitor.py
```

The first time you run it, you will be prompted: 
text
❌ The .env file was not found. A template has been created for you. Please edit the .env file and fill in the correct URL before running the script again.
At this point, edit the generated .env file and enter the Webhook address of your Enterprise WeChat/DingTalk/FlyBook robot: 
text
url=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxx

## 4. Operation Monitoring
Run the script again: 
bash
python monitor.py
The script will start collecting system metrics and display them in real time on the terminal. When the CPU, memory or disk usage exceeds the threshold, an alert message will be automatically sent via Webhook.

## 5. Running in the background (optional)
If you want the script to run continuously in the background, you can use the following method: 
Using nohup: 
bash
nohup python monitor.py > monitor.log 2>&1 &

## 6. Stop Monitoring
If it is running on the front end, simply press Ctrl+C to stop. 
If it is running in the background, use the command "ps aux | grep monitor.py" to find the process ID and then kill it.