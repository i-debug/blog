from django.core.management.base import BaseCommand
from content.models import Category, Article

class Command(BaseCommand):
    help = '列出Omdia 48th Display Japan Forum文章标题'

    def handle(self, *args, **options):
        try:
            # 获取Omdia分类
            omdia_category = Category.objects.get(slug='omdia-display-forum')
            
            # 获取该分类下的所有文章
            articles = Article.objects.filter(category=omdia_category)
            
            self.stdout.write(f'找到 {articles.count()} 篇Omdia论坛文章:')
            for article in articles:
                self.stdout.write(f'- {article.title}')
                
        except Category.DoesNotExist:
            self.stdout.write(
                self.style.WARNING('Omdia分类不存在')
            ) 