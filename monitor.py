"""
思路：
    1.导入模块：psutil、time、datetime、request
    2.定义定时查询函数
    3.定义requests函数
    4.定义报警函数
"""

# 导入模块
import json
import os
import psutil
import requests
import datetime
import time
from dotenv import load_dotenv

# 加载./env的值
env_file = '.env'
if not os.path.exists(env_file):
    with open(env_file, 'w') as f:
        f.write('# 请填写你的 Webhook URL\n')
        f.write('url=你的实际Webhook地址\n')
    print(f"❌ 未找到 {env_file} 文件，已为你创建模板。请编辑 {env_file} 填写正确的 URL 后重新运行脚本。")
    exit(1)

load_dotenv()

# 读取 JSON 配置文件
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 从配置中获取值
THRESHOLDS = config['thresholds']
CPU_MAXUSE = THRESHOLDS['cpu']
MEMORY_MAXUSE = THRESHOLDS['memory']
DISK_MAXUSE = THRESHOLDS['disk']
INTERVAL = config.get('interval', 3)  # 默认3秒获取一次信息
DISK_PATH = config.get('disk_path', '/')
LOG_PATH = config.get('log_file', 'logger_daily.log')  # 获取定义的log存放位置
URL = os.getenv('url')  # 从环境变量读取

# 检查必要的配置是否存在
if not URL:
    raise ValueError("url 环境变量未设置，请在 .env 文件中定义")


# 　定义日志函数
def log_alter(system_time, resource, use):
    message = f'当前系统时间{system_time},设备[{resource}]使用率超过{use}%'
    header = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    try:
        response = requests.post(url=URL, headers=header, json=data)
        if response.status_code == 200:
            print('发送成功')
        else:
            print('发送失败')
    except:
        print('没发送过去')


# 定义使用率告警
def use_alter():
    system_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 获取CPU、内存、磁盘使用率
    cpu_use = psutil.cpu_percent(interval=1)
    if cpu_use >= CPU_MAXUSE:
        print(f'CPU使用率超过阈值{CPU_MAXUSE}%,当前使用率{cpu_use}%')
        log_alter(system_time, 'CPU', CPU_MAXUSE)

    free_use = psutil.virtual_memory().percent
    if free_use >= MEMORY_MAXUSE:
        print(f'内存使用率超过阈值{MEMORY_MAXUSE}%,当前使用率{free_use}%')
        log_alter(system_time, '内存', MEMORY_MAXUSE)

    disk_use = psutil.disk_usage(DISK_PATH).percent
    if disk_use >= DISK_MAXUSE:
        print(f'磁盘使用率超过阈值{DISK_MAXUSE}%,当前使用率{disk_use}%')
        log_alter(system_time, '磁盘', DISK_MAXUSE)

    # 求磁盘读写IO次数与时间与网络接收发送字节
    disk_io1 = psutil.disk_io_counters()
    time.sleep(1)
    disk_io2 = psutil.disk_io_counters()
    # 求写入IO次数及速率
    disk_io_write = (disk_io2.write_bytes - disk_io1.write_bytes) // 1000 ** 2
    disk_io_write_count = disk_io2.write_count - disk_io1.write_count
    # 求读出IO
    disk_io_read = (disk_io2.read_bytes - disk_io1.read_bytes) // 1000 ** 2
    disk_io_read_count = (disk_io2.read_count - disk_io1.read_count)

    # 网络
    network_rs1 = psutil.net_io_counters()
    time.sleep(1)
    network_rs2 = psutil.net_io_counters()

    # 求网络接受与发送字节
    network_resv_b = (network_rs2.bytes_recv - network_rs1.bytes_recv) // 1000 ** 2
    network_send_b = (network_rs2.bytes_sent - network_rs1.bytes_sent) // 1000 ** 2

    # 输出全部设备使用率
    print(
        f'当前时间{system_time}       CPU使用率{cpu_use}%    内存使用率{free_use}%     磁盘使用率{disk_use}%       磁盘读写{disk_io_read:.1f}MB/s {disk_io_write:.1f}MB/s    次数{disk_io_read_count}  {disk_io_write_count}'
        f'    网络发送字节为{network_send_b}Mb/s 接受字节为{network_resv_b}Mb/s')
    logger_alter(system_time, cpu_use, free_use, disk_use)


def logger_alter(system_time, cpu, free, disk):
    # 确保日志文件所在的目录存在
    log_dir = os.path.dirname(LOG_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)  # 自动创建目录

    with open(LOG_PATH, 'a', encoding='utf-8') as file:
        file.write(f'当前时间{system_time}   CPU使用率{cpu}%    内存使用率{free}%     磁盘使用率{disk}% \t \n')


if __name__ == '__main__':
    try:
        while True:
            use_alter()
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print('采集结束')
