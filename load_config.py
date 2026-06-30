import os, json, pymysql
from dotenv import load_dotenv

def load_config():
    # 1. 优先从环境变量读取阈值等基础配置
    CPU_MAXUSE = int(os.getenv('CPU_MAXUSE', '80'))
    MEMORY_MAXUSE = int(os.getenv('MEMORY_MAXUSE', '90'))
    DISK_MAXUSE = int(os.getenv('DISK_MAXUSE', '80'))
    INTERVAL = int(os.getenv('INTERVAL', '3'))
    ALTER_INTERVAL = int(os.getenv('ALTER_INTERVAL', '5'))
    DISK_PATH = os.getenv('DISK_PATH', '/')
    URL = os.getenv('URL')   # webhook
    LOG_PATH = os.getenv('LOG_PATH', '/dev/stdout')

    # 2. 读取 MySQL 连接信息（从环境变量）
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))
    MYSQL_USER = os.getenv('MYSQL_USER', 'monitorer')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '123456')
    MYSQL_DB = os.getenv('MYSQL_DB', 'system_monitor')

    # 连接数据库（如果设置了环境变量）
    conn = None
    cursor = None
    if MYSQL_HOST:
        try:
            conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, port=MYSQL_PORT,
                                   password=MYSQL_PASSWORD, database=MYSQL_DB, charset='utf8mb4')
            cursor = conn.cursor()
        except Exception as e:
            print(f"MySQL 连接失败: {e}，将跳过数据库写入。")

    return {
        'CPU_MAXUSE': CPU_MAXUSE,
        'MEMORY_MAXUSE': MEMORY_MAXUSE,
        'DISK_MAXUSE': DISK_MAXUSE,
        'INTERVAL': INTERVAL,
        'DISK_PATH': DISK_PATH,
        'LOG_PATH': LOG_PATH,
        'ALTER_INTERVAL': ALTER_INTERVAL,
        'URL': URL,
        'conn': conn,
        'cursor': cursor,
        'MYSQL_CONN': {'host': MYSQL_HOST, 'user': MYSQL_USER, 'port': MYSQL_PORT, 'password': MYSQL_PASSWORD, 'database': MYSQL_DB}
    }
