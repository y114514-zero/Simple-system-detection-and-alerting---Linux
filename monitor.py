# 导入模块
import json
import os
import psutil
import requests
import datetime
import time
import pymysql
import prometheus_client
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

# 从配置中获取值mon
THRESHOLDS = config['thresholds']
MYSQL_CONN = config.get('mysql')
INTERVAL = config.get('interval', 3)  # 默认3秒获取一次信息
DISK_PATH = config.get('disk_path', '/')
LOG_PATH = config.get('log_file', 'logger_daily.log')  # 获取定义的log存放位置
ALTER_INTERVAL = config.get('alter_interval', 10)  # 添加告警间隔，默认10s能秒
CPU_MAXUSE = THRESHOLDS['cpu']
MEMORY_MAXUSE = THRESHOLDS['memory']
DISK_MAXUSE = THRESHOLDS['disk']
URL = os.getenv('url')  # 从环境变量读取

# ==========================================定义Prometheus对象==========================================
cpu_use_gauge = prometheus_client.Gauge("CPU_use_percent", "CPU的使用率")
free_use_gauge = prometheus_client.Gauge("Free_use_percent", "内存使用率")
disk_use_gauge = prometheus_client.Gauge("Disk_use_percent", "磁盘使用率")
disk_read_gauge = prometheus_client.Gauge("Disk_read_MB", "磁盘读取数")
disk_write_gauge = prometheus_client.Gauge("Disk_write_MB", "磁盘写入数")
network_send_gauge = prometheus_client.Gauge("Network_send_Mb", "网络发送字节数")
network_resv_gauge = prometheus_client.Gauge("Network_resv_Mb", "网络接受字节数")

# 设置端口号
prometheus_client.start_http_server(8000)
print("Prometheus used port8000")
# ==========================================定义Prometheus对象==========================================

# ==========================================定义MySQL==========================================
# 获取配置文件的mysql参数
if MYSQL_CONN:
    # 与数据库建立连接
    conn = pymysql.connect(
        host=MYSQL_CONN['host'],
        user=MYSQL_CONN['user'],
        port=MYSQL_CONN['port'],
        password=MYSQL_CONN['password'],
        database=MYSQL_CONN['database'],
        charset='utf8mb4'
    )
    cursor = conn.cursor()  # 创建游标对象
# ==========================================定义MySQL==========================================

# 告警初始化（字典）
last_alter_dev = {
    'cpu': 0.0,
    'free': 0.0,
    'disk': 0.0
}

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


# ==========================================定义使用率告警==========================================
def use_alter():
    connect_time = time.time()  # 获取当前时间

    system_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 获取CPU、内存、磁盘使用率
    cpu_use = psutil.cpu_percent(interval=1)
    if cpu_use >= CPU_MAXUSE:
        # 如果当前时间减去上次cpu执行的时间间隔大于告警时间间隔，就会执行以下语句
        if connect_time - last_alter_dev['cpu'] >= ALTER_INTERVAL:
            print(f'CPU使用率超过阈值{CPU_MAXUSE}%,当前使用率{cpu_use}%')
            log_alter(system_time, 'CPU', CPU_MAXUSE)
            # 最后一次cpu时间继承当前时间
            last_alter_dev['cpu'] = connect_time

    free_use = psutil.virtual_memory().percent
    if free_use >= MEMORY_MAXUSE:
        if connect_time - last_alter_dev['free'] >= ALTER_INTERVAL:
            print(f'内存使用率超过阈值{MEMORY_MAXUSE}%,当前使用率{free_use}%')
            log_alter(system_time, '内存', MEMORY_MAXUSE)
            last_alter_dev['free'] = connect_time

    disk_use = psutil.disk_usage(DISK_PATH).percent
    if disk_use >= DISK_MAXUSE:
        if connect_time - last_alter_dev['disk'] >= ALTER_INTERVAL:
            print(f'磁盘使用率超过阈值{DISK_MAXUSE}%,当前使用率{disk_use}%')
            log_alter(system_time, '磁盘', DISK_MAXUSE)
            last_alter_dev['disk'] = connect_time

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

    # ==========================================更新Prometheus指标==========================================
    cpu_use_gauge.set(cpu_use)
    free_use_gauge.set(free_use)
    disk_use_gauge.set(disk_use)
    disk_read_gauge.set(disk_io_read)
    disk_write_gauge.set(disk_io_write)
    network_send_gauge.set(network_send_b)
    network_resv_gauge.set(network_resv_b)
    # ==========================================更新Prometheus指标==========================================

    # ==========================================插入数据==========================================
    if MYSQL_CONN:
        sql = """
            insert into metrics 
            (timestamp, cpu_usage, memory_usage, disk_usage, disk_read_mb, disk_write_mb, disk_read_count,
            disk_write_count, net_send_mb, net_resv_mb)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # 执行修改参数
        cursor.execute(sql, (
            system_time, cpu_use, free_use, disk_use, disk_io_read, disk_io_write, disk_io_read_count,
            disk_io_write_count
            , network_send_b, network_resv_b))

        conn.commit()  # 用来确认更改

        # 清理数据
        if cursor.lastrowid % 127 == 0:
            cursor.execute("TRUNCATE TABLE metrics")
            conn.commit()
            print("数据超过127条，执行清除")


# ==========================================创建日志写入函数==========================================
def logger_alter(system_time, cpu, free, disk):
    # 确保日志文件所在的目录存在
    log_dir = os.path.dirname(LOG_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)  # 自动创建目录

    with open(LOG_PATH, 'a', encoding='utf-8') as file:
        file.write(f'当前时间{system_time}   CPU使用率{cpu}%    内存使用率{free}%     磁盘使用率{disk}% \t \n')


# ==========================================程序入口==========================================
if __name__ == '__main__':
    try:
        while True:
            use_alter()
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print('采集结束')
