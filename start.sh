#!/bin/bash

# 设置环境变量
export DJANGO_SETTINGS_MODULE=blog.settings

# 激活虚拟环境（如果有的话）
# source .venv/bin/activate

# 创建日志目录
mkdir -p logs

# 收集静态文件
echo "收集静态文件..."
python blog/manage.py collectstatic --noinput

# 应用数据库迁移
echo "应用数据库迁移..."
python blog/manage.py migrate

# 检查服务器IP地址
SERVER_IP=$(curl -s ifconfig.me)
echo "服务器IP地址: $SERVER_IP"

# 创建或更新.env文件中的ALLOWED_HOSTS
if [ -f .env ]; then
    # 如果.env文件存在，更新ALLOWED_HOSTS
    if grep -q "ALLOWED_HOSTS" .env; then
        sed -i "s/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=127.0.0.1,localhost,$SERVER_IP/" .env
    else
        echo "ALLOWED_HOSTS=127.0.0.1,localhost,$SERVER_IP" >> .env
    fi
else
    # 如果.env文件不存在，创建一个新的
    echo "DEBUG=False" > .env
    echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')" >> .env
    echo "ALLOWED_HOSTS=127.0.0.1,localhost,$SERVER_IP" >> .env
fi

# 启动 Gunicorn
echo "启动 Gunicorn..."
gunicorn -c gunicorn_config.py blog.wsgi:application 