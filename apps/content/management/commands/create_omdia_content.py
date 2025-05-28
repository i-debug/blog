from django.core.management.base import BaseCommand
from content.models import Category, Article
import os
from pathlib import Path
import re
import unicodedata

class Command(BaseCommand):
    help = '创建Omdia 48th Display Japan Forum内容'

    def handle(self, *args, **options):
        # 创建Omdia分类
        omdia_category, created = Category.objects.get_or_create(
            slug='omdia-display-forum',
            defaults={
                'name': 'Omdia 48th Display Japan Forum',
                'description': '2025年1月23-24日，Omdia第48届日本显示论坛的演讲内容和分析',
                'icon': 'fas fa-tv',
                'order': 10
            }
        )
        
        if created:
            self.stdout.write(f'创建分类: {omdia_category.name}')
        else:
            self.stdout.write(f'更新分类: {omdia_category.name}')
        
        # 获取Omdia文件夹的路径
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        omdia_dir = base_dir / 'content_files' / '20250123-24_Omdia 48th Display Japan Forum'
        
        self.stdout.write(f'查找目录: {omdia_dir}')
        
        if not omdia_dir.exists():
            self.stdout.write(self.style.ERROR(f'目录不存在: {omdia_dir}'))
            return
        
        # 遍历文件夹中的HTML文件
        all_files = list(omdia_dir.glob('*.html'))
        self.stdout.write(f'找到 {len(all_files)} 个HTML文件')
        
        for html_file in all_files:
            file_name = html_file.name
            self.stdout.write(f'处理文件: {file_name}')
            
            try:
                # 从文件名中提取标题
                match = re.match(r'(\d+-\d+)\s+(.*?)\.html', file_name)
                if match:
                    session_id = match.group(1)
                    title_content = match.group(2)
                    
                    # 完整标题包含会话ID
                    title = f"{session_id} {title_content}"
                    
                    self.stdout.write(f'  会话ID: {session_id}, 标题: {title}')
                    
                    # 创建ASCII兼容的slug
                    # 1. 将非ASCII字符转换为ASCII或删除
                    normalized_title = unicodedata.normalize('NFKD', title_content)
                    ascii_title = ''.join([c for c in normalized_title if not unicodedata.combining(c) and ord(c) < 128])
                    
                    # 2. 只保留字母、数字、空格和连字符
                    clean_title = re.sub(r'[^\w\s-]', '', ascii_title).strip().lower()
                    
                    # 3. 将空格替换为连字符
                    slug_title = re.sub(r'\s+', '-', clean_title)
                    
                    # 4. 组合最终slug
                    slug = f"omdia-{session_id.replace('-', '')}-{slug_title}"
                    
                    self.stdout.write(f'  生成的slug: {slug}')
                    
                    # 创建摘要
                    summary = f"Omdia第48届日本显示论坛演讲：{title_content}。会议编号：{session_id}"
                    
                    # 提取演讲者和主题
                    speaker_match = re.search(r'(.*?)\s*-\s*(.*)', title_content)
                    if speaker_match:
                        speaker = speaker_match.group(1).strip()
                        topic = speaker_match.group(2).strip()
                        tags = f"Omdia, Display Forum, {speaker}, {topic.split(' ')[0]}"
                    else:
                        tags = "Omdia, Display Forum, 显示技术"
                    
                    # 创建文章
                    article, created = Article.objects.get_or_create(
                        slug=slug[:100],  # 确保slug不超过100个字符
                        defaults={
                            'title': title,
                            'category': omdia_category,
                            'summary': summary,
                            'html_file_path': str(html_file),
                            'tags': tags,
                            'is_featured': session_id in ['1-01', '2-01'],  # 将第一个演讲设为推荐
                            'is_published': True
                        }
                    )
                    
                    if created:
                        self.stdout.write(f'创建文章: {article.title}')
                    else:
                        self.stdout.write(f'更新文章: {article.title}')
                else:
                    self.stdout.write(self.style.WARNING(f'  无法解析文件名: {file_name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  处理文件 {file_name} 时出错: {str(e)}'))
        
        self.stdout.write(
            self.style.SUCCESS('Omdia 48th Display Japan Forum内容创建完成！')
        ) 