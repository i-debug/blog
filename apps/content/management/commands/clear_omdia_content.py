from django.core.management.base import BaseCommand
from content.models import Category, Article

class Command(BaseCommand):
    help = '清除Omdia 48th Display Japan Forum内容'

    def handle(self, *args, **options):
        try:
            # 获取Omdia分类
            omdia_category = Category.objects.get(slug='omdia-display-forum')
            
            # 删除该分类下的所有文章
            count, _ = Article.objects.filter(category=omdia_category).delete()
            
            self.stdout.write(
                self.style.SUCCESS(f'成功删除 {count} 篇Omdia论坛文章')
            )
        except Category.DoesNotExist:
            self.stdout.write(
                self.style.WARNING('Omdia分类不存在，无需清除')
            ) 