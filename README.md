一个轻量级的系统资源监控与告警工具，支持**单机运行**和 **Kubernetes 集群部署**。  
实时采集 CPU、内存、磁盘、网络指标，超过阈值时通过企业微信/钉钉/飞书 Webhook 发送告警，并可调用 **DeepSeek 等大模型进行 AI 根因分析**。

---

## ✨ 核心功能

- **实时系统监控**：持续采集 CPU、内存、磁盘空间的使用率，以及磁盘读写速率、网络流量等。
- **阈值告警**：通过配置文件自定义告警阈值，超出后自动发送 Webhook 通知。
- **AI 智能分析**（可选）：发生告警时，自动调用 LLM（大语言模型）分析历史数据，给出排查建议并附加到告警消息中。
- **多平台运行**：原生 Python 脚本可在 Linux / macOS / Windows 上运行。
- **Kubernetes 原生支持**：提供 Dockerfile 和 K8s 资源清单（DaemonSet、Service、ConfigMap、Secret、ServiceMonitor），轻松部署为集群节点监控。
- **Prometheus + Grafana 集成**：指标暴露为 Prometheus 格式，可被 Prometheus 抓取并在 Grafana 中可视化。
- **日志记录**：关键指标输出到标准输出（容器化）或本地日志文件（单机），便于排查。
- **自动配置模板**：首次运行自动创建 `.env` 和 `config.json` 模板（仅单机模式）。

---

## 🛠️ 技术栈

- 编程语言：Python 3.9+
- 核心依赖：
  - `psutil`：采集系统资源信息
  - `requests`：发送 HTTP 告警请求
  - `prometheus_client`：暴露 Prometheus 指标
  - `pymysql`：可选，写入 MySQL 历史数据
  - `openai`：对接 DeepSeek 等 OpenAI 兼容 API，实现 AI 分析
- 配置格式：JSON (config.json) 与环境变量文件 (.env)（单机）；ConfigMap + Secret（Kubernetes）
- 容器编排：Docker / Kubernetes (DaemonSet)

---

## ⭐️ 快速开始（单机/传统部署）

### 1. 克隆仓库

```
git clone https://github.com/y114514-zero/Simple-system-detection-and-alerting---Linux.git
cd Simple-system-detection-and-alerting---Linux
```

### 2. 安装依赖
推荐使用虚拟环境：


```
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
# 或 .\venv\Scripts\activate  # Windows
pip install -r requirements.txt

```

### 3. 配置

config.json：修改阈值、采集间隔、日志路径等（默认值通常可用）。
.env：首次运行脚本会自动生成模板，编辑填入 Webhook URL（必填）和 AI API Key（可选）。

```
url=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxx
API_KEY=sk-your-deepseek-api-key   # 如需 AI 分析
```

### 4. 运行监控

`python monitor.py`
终端会实时显示采集指标，超过阈值时自动发送告警。

### 5. 后台运行（可选）

> nohup python monitor.py > monitor.log 2>&1 &

## 🚢Kubernetes 部署
前置条件
Kubernetes 集群（v1.20+）

已安装网络插件（如 Flannel、Calico），并确保 Pod 可以访问外网（若 Flannel 须启用 EnableSNAT，并调整 MTU 到 1400）。

（可选）已部署 Prometheus Operator + Grafana（如需可视化）。
### 1. 构建镜像

```
docker build -t your-registry/simple-monitor:v1 .
docker push your-registry/simple-monitor:v1
```

修改 k8s/daemonset.yaml 中的镜像地址。

### 2. 修改 K8s 资源配置
根据你的环境编辑 k8s/ 目录下的 YAML 文件：

configmap.yaml：调整告警阈值、MySQL 地址（若不用可忽略）、采集间隔等。
secret.yaml：填入真实的 Webhook URL、DeepSeek API Key 等敏感信息。
daemonset.yaml：若需固定外网域名 IP，添加 hostAliases（详见下文网络问题处理）。

### 3. 部署

```
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/daemonset.yaml
kubectl apply -f k8s/service.yaml
# 如果使用 Prometheus Operator
kubectl apply -f k8s/servicemonitor.yaml
```

### 4. 验证

```
kubectl get pods -n monitoring
kubectl logs -n monitoring <pod-name> -f
```
可以看到实时采集输出，如果硬件超过阈值就会触发告警。

### 5. Prometheus + Grafana 集成
ServiceMonitor 会自动被发现（标签匹配 release: kube-prometheus-stack）。
在 Grafana 中创建 Dashboard，查询 CPU_use_percent、Free_use_percent 等指标即可。

### 6. 常见网络问题
Pod 无法访问外网：Flannel 需在 ConfigMap 中设置 "EnableSNAT": true。

HTTPS 连接超时：可能因 MTU 过大，在 Flannel ConfigMap 中设置 "MTU": 1400。

部分 CDN IP 不通：使用 hostAliases 将域名固定到可达 IP，例如：


```
hostAliases:
- ip: "117.135.156.58"
  hostnames:
  - "qyapi.weixin.qq.com"
- ip: "<deepseek可达IP>"
  hostnames:
  - "api.deepseek.com"
```

## 🧠 AI 告警说明
当启用 AI 分析后（设置 API_KEY），告警触发时会：

查询 MySQL 中最近 10 条该资源的历史数据（若数据库可用）；

将资源类型、当前值、阈值和历史数据发送给大模型；

大模型返回可能的原因及排查建议；

告警消息中附带 AI 分析结果。

目前仅支持 OpenAI 兼容接口（如 DeepSeek、OpenAI 官方），代码在 AI.py 中，可按需修改 Prompt。

## 📊 架构图（Kubernetes 模式）


```
┌──────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ Node1    │  │ Node2    │  │ Node3    │            │
│  │ DaemonSet│  │ DaemonSet│  │ DaemonSet│            │
│  │ Pod      │  │ Pod      │  │ Pod      │            │
│  │ :8000    │  │ :8000    │  │ :8000    │            │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
│       │  采集宿主机指标 (psutil)     │                │
│       └──────────────────┬──────────────────┘        │
│                          ▼                           │
│              ┌─────────────────────┐                 │
│              │   Prometheus        │                 │
│              │   (抓取 /metrics)    │                │
│              └────────┬────────────┘                 │
│                       │ 查询                         │
│              ┌────────▼────────────┐                 │
│              │      Grafana        │                 │
│              └─────────────────────┘                 │
│                       │                              │
│                       ▼ (阈值触发)                    │
│              ┌─────────────────────┐                 │
│              │ 告警 + AI 分析      │                  │
│              │ ├→ 企业微信 Webhook  │                 │
│              │ └→ DeepSeek API     │                 │
│              └─────────────────────┘                 │
│                                                      │
│  配置注入: ConfigMap (阈值等) + Secret (密钥/URL)      │
└──────────────────────────────────────────────────────┘
```

## 📁 项目文件结构（K8s 容器化后）


```
> .
> ├── AI.py
> ├── alter.py
> ├── history.py
> ├── load_config.py
> ├── logger.py
> ├── monitor.py
> ├── mysql_config.py
> ├── Prometheus_config.py
> ├── requirements.txt
> ├── Dockerfile
> ├── .dockerignore
> ├── config.json                 # 单机使用，容器内不再依赖
> ├── logs/                       # 单机日志目录
> └── k8s/
>     ├── namespace.yaml
>     ├── configmap.yaml
>     ├── secret.yaml
>     ├── daemonset.yaml
>     ├── service.yaml
>     └── servicemonitor.yaml
```


## 🔧 配置说明（Kubernetes 环境变量）

```
环境变量	说明	默认值
CPU_MAXUSE	CPU 告警阈值 (%)	80
MEMORY_MAXUSE	内存告警阈值 (%)	90
DISK_MAXUSE	磁盘告警阈值 (%)	80
INTERVAL	采集间隔 (秒)	3
ALTER_INTERVAL	同一资源告警最小间隔 (秒)	5
DISK_PATH	磁盘监控路径	/
MYSQL_HOST	MySQL 主机地址（留空则不写库）	mysql-service
MYSQL_PORT	MySQL 端口	3306
MYSQL_USER	MySQL 用户名	monitorer
MYSQL_PASSWORD	MySQL 密码	123456
MYSQL_DB	MySQL 数据库名	system_monitor
URL	Webhook 完整地址	-
API_KEY	DeepSeek/OpenAI API Key	-
API_URL	API 基础地址	https://api.deepseek.com/v1
MODEL_NAME	模型名	deepseek-reasoner
LOG_PATH	日志输出路径（容器内建议 /dev/stdout）	/dev/stdout
```


## 🎯 停止监控
单机模式：前台运行时按 Ctrl+C；后台则 ps aux | grep monitor.py 并 kill。

K8s 模式：删除 DaemonSet

`kubectl delete daemonset node-monitor -n monitoring`

## 📄 License
本项目基于 MIT License 开源，欢迎自由使用和修改。
