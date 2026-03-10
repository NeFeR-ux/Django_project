from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.flatpages.models import FlatPage
from .models import Post, Category, Author
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.models import Group


@login_required
def become_author(request):
    """Функция для добавления пользователя в группу authors"""
    authors_group = Group.objects.get(name='authors')
    request.user.groups.add(authors_group)
    messages.success(request, 'Теперь вы автор!')
    return redirect('news_list')

def page1(request):
    flatpage = get_object_or_404(FlatPage, url='/page1/')
    return render(request, 'pages/page1.html', {'flatpage': flatpage})

def page2(request):
    return render(request, 'pages/page2.html')

@login_required
def page3(request):
    return render(request, 'pages/page3.html')

def test(request):
    return render(request, 'flatpages/test.html')

def news_list(request):
    """Список всех новостей"""
    news = Post.objects.filter(post_type='NW')  # NW = новость
    return render(request, 'pages/news_list.html', {'news': news})

def news_detail(request, news_id):
    """Детальная страница новости"""
    news_item = get_object_or_404(Post, id=news_id, post_type='NW')
    return render(request, 'pages/news_detail.html', {'news': news_item})


# Список новостей с пагинацией
def news_list(request):
    news = Post.objects.filter(post_type='NW').order_by('-created_at')
    paginator = Paginator(news, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pages/news_list.html', {'page_obj': page_obj})


# Поиск новостей
def news_search(request):
    news = Post.objects.filter(post_type='NW').order_by('-created_at')
    filter = PostFilter(request.GET, queryset=news)

    paginator = Paginator(filter.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/news_search.html', {
        'filter': filter,
        'page_obj': page_obj
    })


# Детальная страница новости
def news_detail(request, pk):
    news = get_object_or_404(Post, id=pk, post_type='NW')
    return render(request, 'pages/news_detail.html', {'news': news})


# Создание новости
class NewsCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'pages/news_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.post_type = 'NW'
        author = Author.objects.get(user=self.request.user)
        form.instance.author = author
        messages.success(self.request, 'Новость успешно создана!')
        return super().form_valid(form)


# Редактирование новости
class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'pages/news_edit.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='NW')

    def form_valid(self, form):
        messages.success(self.request, 'Новость успешно обновлена!')
        return super().form_valid(form)


# Удаление новости
class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'pages/news_confirm_delete.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='NW')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Новость удалена!')
        return super().delete(request, *args, **kwargs)


# Аналогично для статей
def article_list(request):
    articles = Post.objects.filter(post_type='AR').order_by('-created_at')
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pages/article_list.html', {'page_obj': page_obj})


def article_detail(request, pk):
    article = get_object_or_404(Post, id=pk, post_type='AR')
    return render(request, 'pages/article_detail.html', {'article': article})


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'pages/article_edit.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        form.instance.post_type = 'AR'
        author = Author.objects.get(user=self.request.user)
        form.instance.author = author
        messages.success(self.request, 'Статья успешно создана!')
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'pages/article_edit.html'
    success_url = reverse_lazy('article_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='AR')


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'pages/article_confirm_delete.html'
    success_url = reverse_lazy('article_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='AR')

@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.add(request.user)
    messages.success(request, f'Вы подписались на категорию "{category.name}"')
    return redirect('news_list')

@login_required
def unsubscribe_from_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.remove(request.user)
    messages.success(request, f'Вы отписались от категории "{category.name}"')
    return redirect('news_list')