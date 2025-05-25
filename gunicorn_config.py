"""Gunicorn 配置文件"""
import multiprocessing

# 绑定的 IP 和端口
bind = "0.0.0.0:8000"

# 工作进程数量
workers = multiprocessing.cpu_count() * 2 + 1

# 工作模式
worker_class = "sync"

# 超时时间
timeout = 120

# 最大请求数
max_requests = 1000
max_requests_jitter = 50

# 日志级别
loglevel = "info"

# 日志文件
accesslog = "logs/access.log"
errorlog = "logs/error.log"

# 守护进程模式
daemon = False

# 进程名称
proc_name = "blog_gunicorn"

# 预加载应用
preload_app = True 