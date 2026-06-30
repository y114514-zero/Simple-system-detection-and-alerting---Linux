FROM python:3.9-slim

# 告警日志
ENV PYTHONUNBUFFERED=1

# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装可能需要的依赖
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# Prometheus 端口
EXPOSE 8000

# 直接运行主程序
CMD ["python", "monitor.py"]
