#!/usr/bin/env python
import os
import django
import re

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.content.models import Article

# 旧路径的前缀（Windows路径）
OLD_PATH_PREFIX = r'D:\Project\blog\blog'

# 新路径的前缀（macOS路径）
NEW_PATH_PREFIX = '/Users/shu/Documents/blog'

# 获取所有文章
articles = Article.objects.all()
updated_count = 0

for article in articles:
    if article.html_file_path and article.html_file_path.startswith(OLD_PATH_PREFIX):
        # 替换路径前缀
        new_path = article.html_file_path.replace(OLD_PATH_PREFIX, NEW_PATH_PREFIX)
        # 替换Windows路径分隔符为Unix路径分隔符
        new_path = new_path.replace('\\', '/')
        
        print(f"更新文章 '{article.title}':")
        print(f"  旧路径: {article.html_file_path}")
        print(f"  新路径: {new_path}")
        
        # 更新路径
        article.html_file_path = new_path
        article.save()
        updated_count += 1

print(f"\n共更新了 {updated_count} 篇文章的路径。") 