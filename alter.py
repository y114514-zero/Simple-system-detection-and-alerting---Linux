import requests


# 定义告警信息
def log_alter(url, system_time, resource, use, advice=None):
    # 默认发送
    message = f'当前系统时间{system_time},设备[{resource}]使用率超过{use}%'
    if advice:  # 如果advice还是默认的None就不会执行AI分析，取决于你想不想使用
        message += f"\n\n🤖 AI 分析建议：\n{advice}"

    header = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    try:
        response = requests.post(url=url, headers=header, json=data)
        if response.status_code == 200:
            print('发送成功')
        else:
            print('发送失败')
    except:
        print('没发送过去')
