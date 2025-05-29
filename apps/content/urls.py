from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('<slug:category_slug>/<slug:article_slug>/', views.article_detail, name='article_detail'),
] 