from django.db import models
from django.utils import timezone
from pathlib import Path
import os

class Category(models.Model):
    """内容分类"""
    name = models.CharField(max_length=100, verbose_name="分类名称")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL标识")
    description = models.TextField(blank=True, verbose_name="分类描述")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Font Awesome图标")
    order = models.IntegerField(default=0, verbose_name="排序")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    
    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class Article(models.Model):
    """文章模型"""
    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('URL', max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles', verbose_name='分类')
    content = models.TextField('内容', blank=True)
    html_file_path = models.CharField('HTML文件路径', max_length=255, blank=True, null=True)
    summary = models.TextField('摘要', blank=True)
    tags = models.CharField('标签', max_length=200, blank=True, help_text='用逗号分隔')
    cover_image = models.ImageField('封面图', upload_to='covers/', blank=True, null=True)
    is_published = models.BooleanField('是否发布', default=True)
    is_featured = models.BooleanField('是否推荐', default=False)
    view_count = models.IntegerField('浏览次数', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('content:article_detail', kwargs={'category_slug': self.category.slug, 'article_slug': self.slug})
    
    def get_tags_list(self):
        """获取标签列表"""
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',')]
    
    def get_html_content(self):
        """读取HTML文件内容"""
        try:
            file_path = Path(self.html_file_path)
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            return f"<p>无法加载内容: {str(e)}</p>"
        return "<p>文件不存在</p>" 