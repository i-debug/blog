import os
import re
from pathlib import Path

def update_cdn_links(file_path):
    """更新HTML文件中的CDN链接为中国大陆提供服务的CDN"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        
        # 替换TailwindCSS CDN
        content = re.sub(
            r'<script src="https://cdn\.tailwindcss\.com.*?</script>',
            '<script src="https://lf6-cdn-tos.bytecdntp.com/cdn/tailwind/3.3.3/tailwind.min.js"></script>',
            content
        )
        
        # 替换Font Awesome CDN
        content = re.sub(
            r'<link.*?href="https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/.*?\.css.*?>',
            '<link rel="stylesheet" href="https://cdn.bootcdn.net/ajax/libs/font-awesome/6.4.0/css/all.min.css">',
            content
        )
        
        # 替换Chart.js CDN
        content = re.sub(
            r'<script src="https://cdn\.jsdelivr\.net/npm/chart\.js.*?</script>',
            '<script src="https://cdn.staticfile.org/Chart.js/4.4.0/chart.umd.min.js"></script>',
            content
        )
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"已更新 {file_path}")
        return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")
        return False

def main():
    """遍历content_files目录下的所有HTML文件并更新CDN链接"""
    # 使用当前工作目录
    base_dir = os.getcwd()
    content_files_dir = os.path.join(base_dir, 'content_files')
    
    print(f"开始更新CDN链接...")
    print(f"当前目录: {base_dir}")
    print(f"内容文件目录: {content_files_dir}")
    
    updated_count = 0
    
    # 遍历所有HTML文件
    for root, dirs, files in os.walk(content_files_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if update_cdn_links(file_path):
                    updated_count += 1
    
    print(f"完成! 已更新 {updated_count} 个文件的CDN链接")

if __name__ == "__main__":
    main() 