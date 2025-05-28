from django.core.management.base import BaseCommand
from content.models import Category, Article
import os
from pathlib import Path

class Command(BaseCommand):
    help = '创建示例数据'

    def handle(self, *args, **options):
        # 创建分类
        categories_data = [
            {
                'name': 'Python开发',
                'slug': 'python',
                'description': '深入探索Python编程语言的各个方面，从基础语法到高级应用',
                'icon': 'fab fa-python',
                'order': 1
            },
            {
                'name': 'Web开发',
                'slug': 'web-dev',
                'description': '现代Web开发技术和最佳实践，包括前端和后端技术',
                'icon': 'fas fa-globe',
                'order': 2
            },
            {
                'name': '数据科学',
                'slug': 'data-science',
                'description': '数据分析、机器学习和人工智能相关技术',
                'icon': 'fas fa-chart-line',
                'order': 3
            },
            {
                'name': '系统架构',
                'slug': 'architecture',
                'description': '软件架构设计、系统设计和技术选型',
                'icon': 'fas fa-sitemap',
                'order': 4
            },
            {
                'name': '工具与效率',
                'slug': 'tools',
                'description': '开发工具、效率提升和工作流优化',
                'icon': 'fas fa-tools',
                'order': 5
            }
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'创建分类: {category.name}')

        # 创建文章
        python_category = Category.objects.get(slug='python')
        web_category = Category.objects.get(slug='web-dev')
        
        # 获取示例HTML文件的绝对路径
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        sample_file_path = base_dir / 'content_files' / 'sample_article.html'
        
        articles_data = [
            {
                'title': 'Python Web开发最佳实践',
                'slug': 'python-web-best-practices',
                'category': python_category,
                'summary': '深入探讨Python Web开发的最佳实践，包括框架选择、环境配置、数据库设计等关键要素。',
                'html_file_path': str(sample_file_path),
                'tags': 'Python, Django, Flask, Web开发, 最佳实践',
                'is_featured': True,
                'is_published': True
            },
            {
                'title': 'Django高级特性详解',
                'slug': 'django-advanced-features',
                'category': python_category,
                'summary': '深入了解Django框架的高级特性，包括中间件、信号、缓存等功能的使用技巧。',
                'html_file_path': str(sample_file_path),
                'tags': 'Django, Python, Web框架, 高级特性',
                'is_featured': True,
                'is_published': True
            },
            {
                'title': '现代前端开发工作流',
                'slug': 'modern-frontend-workflow',
                'category': web_category,
                'summary': '构建高效的现代前端开发工作流，包括工具链选择、自动化构建和部署策略。',
                'html_file_path': str(sample_file_path),
                'tags': 'JavaScript, 前端开发, 工作流, 自动化',
                'is_featured': False,
                'is_published': True
            },
            {
                'title': 'RESTful API设计指南',
                'slug': 'restful-api-design-guide',
                'category': web_category,
                'summary': '设计优雅、可维护的RESTful API的完整指南，包括最佳实践和常见陷阱。',
                'html_file_path': str(sample_file_path),
                'tags': 'API, REST, Web服务, 设计模式',
                'is_featured': True,
                'is_published': True
            }
        ]

        for article_data in articles_data:
            article, created = Article.objects.get_or_create(
                slug=article_data['slug'],
                defaults=article_data
            )
            if created:
                self.stdout.write(f'创建文章: {article.title}')

        self.stdout.write(
            self.style.SUCCESS('示例数据创建完成！')
        ) 