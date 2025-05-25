# 博客项目IP访问部署指南

本文档提供将博客项目部署到生产环境并通过IP地址访问的详细步骤。

## 准备工作

1. 一台 Linux 服务器（推荐 Ubuntu 22.04 LTS）
2. 服务器有公网IP地址
3. Python 3.10+ 环境

## 部署步骤

### 1. 安装必要软件

```bash
# 更新系统
sudo apt update
sudo apt upgrade -y

# 安装依赖
sudo apt install -y python3-pip python3-venv nginx
```

### 2. 克隆项目

```bash
# 创建项目目录
mkdir -p /var/www
cd /var/www

# 克隆项目
git clone <your-repository-url> blog
cd blog
```

### 3. 设置虚拟环境

```bash
# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 4. 创建环境变量文件

```bash
# 创建环境变量文件
cat > .env << EOL
DEBUG=False
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')
ALLOWED_HOSTS=127.0.0.1,localhost,$(curl -s ifconfig.me)
DATABASE_URL=sqlite:///db.sqlite3
EOL
```

### 5. 收集静态文件

```bash
# 创建日志目录
mkdir -p logs

# 收集静态文件
python blog/manage.py collectstatic --noinput

# 应用数据库迁移
python blog/manage.py migrate
```

### 6. 配置 Nginx

```bash
# 复制 Nginx 配置文件
cp nginx_ip.conf.example /etc/nginx/sites-available/blog

# 编辑 Nginx 配置
sudo nano /etc/nginx/sites-available/blog
```

修改配置文件中的以下内容：

- 更新静态文件路径：将 `/path/to/your/project/staticfiles/` 替换为 `/var/www/blog/blog/staticfiles/`
- 更新媒体文件路径：将 `/path/to/your/project/media/` 替换为 `/var/www/blog/blog/media/`

```bash
# 启用网站配置
sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default  # 移除默认配置
sudo nginx -t  # 测试配置
sudo systemctl restart nginx
```

### 7. 配置 Gunicorn 服务

```bash
# 复制 systemd 服务文件
cp blog.service.example /etc/systemd/system/blog.service

# 编辑服务文件
sudo nano /etc/systemd/system/blog.service
```

修改服务文件中的以下内容：

- 将 `WorkingDirectory=/path/to/your/project` 替换为 `WorkingDirectory=/var/www/blog`
- 将 `ExecStart=/path/to/your/venv/bin/gunicorn` 替换为 `ExecStart=/var/www/blog/.venv/bin/gunicorn`

```bash
# 启用并启动服务
sudo systemctl daemon-reload
sudo systemctl enable blog
sudo systemctl start blog
sudo systemctl status blog
```

### 8. 设置防火墙（如果启用）

```bash
# 允许 HTTP 流量
sudo ufw allow 80/tcp

# 如果需要SSH访问
sudo ufw allow 22/tcp

# 启用防火墙
sudo ufw enable
```

### 9. 设置权限

```bash
# 设置适当的文件权限
sudo chown -R www-data:www-data /var/www/blog
sudo chmod -R 755 /var/www/blog
sudo chown -R www-data:www-data logs
```

## 访问您的博客

部署完成后，您可以通过服务器的IP地址访问博客：

```
http://your-server-ip
```

## 维护命令

### 重启服务

```bash
sudo systemctl restart blog
sudo systemctl restart nginx
```

### 查看日志

```bash
# Gunicorn 日志
tail -f logs/error.log
tail -f logs/access.log

# Nginx 日志
tail -f /var/log/nginx/blog_error.log
tail -f /var/log/nginx/blog_access.log
```

### 更新代码

```bash
cd /var/www/blog
git pull
source .venv/bin/activate
pip install -r requirements.txt
python blog/manage.py collectstatic --noinput
python blog/manage.py migrate
sudo systemctl restart blog
```

## 故障排除

### 服务无法启动

检查日志文件：

```bash
sudo journalctl -u blog.service
```

### 静态文件无法加载

确保路径配置正确：

```bash
ls -la /var/www/blog/blog/staticfiles
sudo nginx -t
```

### 无法通过IP访问

检查防火墙设置：

```bash
sudo ufw status
```

检查Nginx是否正在运行：

```bash
sudo systemctl status nginx
```

检查IP地址是否正确：

```bash
curl -s ifconfig.me
``` 