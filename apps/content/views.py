from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Q
from .models import Category, Article
import os

def home(request):
    """首页视图"""
    # 获取推荐文章
    featured_articles = Article.objects.filter(is_published=True, is_featured=True)[:6]
    
    # 获取所有分类及其文章数量
    categories = Category.objects.all()
    
    # 获取最新文章
    recent_articles = Article.objects.filter(is_published=True)[:8]
    
    # 获取Omdia论坛文章
    try:
        omdia_category = Category.objects.get(slug='omdia-display-forum')
        omdia_featured_articles = Article.objects.filter(
            category=omdia_category,
            is_published=True,
            is_featured=True
        )[:2]
        
        omdia_other_articles = Article.objects.filter(
            category=omdia_category,
            is_published=True
        ).exclude(
            id__in=[article.id for article in omdia_featured_articles]
        )[:8]
    except Category.DoesNotExist:
        omdia_featured_articles = []
        omdia_other_articles = []
    
    context = {
        'featured_articles': featured_articles,
        'categories': categories,
        'recent_articles': recent_articles,
        'omdia_featured_articles': omdia_featured_articles,
        'omdia_other_articles': omdia_other_articles,
    }
    return render(request, 'content/home.html', context)

def category_detail(request, category_slug):
    """分类详情页视图"""
    category = get_object_or_404(Category, slug=category_slug)
    articles = Article.objects.filter(category=category, is_published=True)
    
    context = {
        'category': category,
        'articles': articles,
    }
    
    # 如果是Omdia论坛分类，使用专用模板
    if category_slug == 'omdia-display-forum':
        return render(request, 'content/omdia_forum.html', context)
    
    return render(request, 'content/category_detail.html', context)

def article_detail(request, category_slug, article_slug):
    """文章详情页视图"""
    article = get_object_or_404(Article, slug=article_slug, category__slug=category_slug)
    
    # 增加文章浏览量
    article.view_count += 1
    article.save()
    
    # 获取相关文章
    related_articles = Article.objects.filter(
        category=article.category, 
        is_published=True
    ).exclude(
        id=article.id
    )[:3]
    
    # 处理HTML文件内容
    html_content = None
    if article.html_file_path and os.path.exists(article.html_file_path):
        try:
            with open(article.html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
        except Exception as e:
            print(f"读取HTML文件错误: {e}")
            # 读取错误时不设置html_content，将使用article.content
    
    context = {
        'article': article,
        'related_articles': related_articles,
        'html_content': html_content,
    }
    
    # 如果是Omdia论坛的文章，使用专用模板
    if category_slug == 'omdia-display-forum':
        return render(request, 'content/omdia_article_detail.html', context)
    
    return render(request, 'content/article_detail.html', context)

def search(request):
    """搜索功能"""
    query = request.GET.get('q', '').strip()
    articles = []
    
    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) | 
            Q(summary__icontains=query) | 
            Q(tags__icontains=query),
            is_published=True
        )
    
    context = {
        'query': query,
        'articles': articles,
    }
    return render(request, 'content/search.html', context) 