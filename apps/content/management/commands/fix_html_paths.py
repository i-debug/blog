import os
from django.core.management.base import BaseCommand
from apps.content.models import Article
from pathlib import Path

class Command(BaseCommand):
    help = '修复文章HTML文件路径'

    def handle(self, *args, **options):
        # 获取项目根目录
        base_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
        content_files_dir = os.path.join(base_dir, 'content_files')
        
        self.stdout.write(f"项目根目录: {base_dir}")
        self.stdout.write(f"内容文件目录: {content_files_dir}")
        
        # 获取所有文章
        articles = Article.objects.all()
        fixed_count = 0
        
        for article in articles:
            if not article.html_file_path:
                continue
                
            # 检查当前路径是否有效
            current_path = article.html_file_path
            if os.path.exists(current_path):
                continue  # 路径有效，不需要修复
                
            # 尝试构建绝对路径
            abs_path = os.path.join(base_dir, article.html_file_path)
            if os.path.exists(abs_path):
                # 更新为绝对路径
                article.html_file_path = abs_path
                article.save()
                fixed_count += 1
                self.stdout.write(self.style.SUCCESS(f"已修复: {article.title} -> {abs_path}"))
                continue
                
            # 尝试在content_files目录中查找
            file_name = os.path.basename(article.html_file_path)
            
            # 在content_files目录及其子目录中搜索文件
            for root, dirs, files in os.walk(content_files_dir):
                for filename in files:
                    if filename == file_name:
                        new_path = os.path.join(root, filename)
                        article.html_file_path = new_path
                        article.save()
                        fixed_count += 1
                        self.stdout.write(self.style.SUCCESS(f"已修复: {article.title} -> {new_path}"))
                        break
            
        self.stdout.write(self.style.SUCCESS(f"已修复 {fixed_count} 篇文章的HTML路径")) 