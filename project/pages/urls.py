from django.urls import path
from . import views

urlpatterns = [
    path('page1/', views.page1, name='page1'),
    path('page2/', views.page2, name='page2'),
    path('page3/', views.page3, name='page3'),
    path('test/', views.test, name='test'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('news/', views.news_list, name='news_list'),
    path('news/search/', views.news_search, name='news_search'),
    path('news/create/', views.NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('news/<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    path('articles/<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('become-author/', views.become_author, name='become_author'),
    path('subscribe/<int:category_id>/', views.subscribe_to_category, name='subscribe'),
    path('unsubscribe/<int:category_id>/', views.unsubscribe_from_category, name='unsubscribe'),
path('test-logging/', views.test_logging, name='test_logging'),
]