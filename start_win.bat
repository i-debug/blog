@echo off
REM Windows环境下的启动脚本

REM 创建日志目录
if not exist logs mkdir logs

REM 设置环境变量
set DJANGO_SETTINGS_MODULE=blog.settings

REM 收集静态文件
echo 收集静态文件...
python blog\manage.py collectstatic --noinput

REM 应用数据库迁移
echo 应用数据库迁移...
python blog\manage.py migrate

REM 启动 Gunicorn (Windows下可能需要使用waitress)
echo 启动服务...
cd blog
python manage.py runserver 0.0.0.0:8000

REM 如果安装了waitress，可以使用以下命令
REM waitress-serve --listen=0.0.0.0:8000 blog.wsgi:application 