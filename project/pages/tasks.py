from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from .models import Category, Post


@shared_task
def send_new_post_notification(post_id):
    """Отправка уведомления о новой статье подписчикам категории"""
    post = Post.objects.get(id=post_id)

    for category in post.categories.all():
        subscribers = category.subscribers.all()

        for subscriber in subscribers:
            html_content = render_to_string(
                'email/new_post_notification.html',
                {
                    'post': post,
                    'subscriber': subscriber,
                    'category': category
                }
            )

            send_mail(
                subject=f'Новая статья в категории {category.name}',
                message='',
                html_message=html_content,
                from_email=None,
                recipient_list=[subscriber.email],
                fail_silently=False,
            )


@shared_task
def send_weekly_newsletter():
    """Еженедельная рассылка новых статей за неделю"""
    week_ago = timezone.now() - timedelta(days=7)

    for category in Category.objects.all():
        subscribers = category.subscribers.all()
        if not subscribers.exists():
            continue

        new_posts = Post.objects.filter(
            categories=category,
            created_at__gte=week_ago
        ).order_by('-created_at')

        if new_posts.exists():
            for subscriber in subscribers:
                html_content = render_to_string(
                    'email/weekly_newsletter.html',
                    {
                        'category': category,
                        'new_posts': new_posts,
                        'subscriber': subscriber
                    }
                )

                send_mail(
                    subject=f'Еженедельная рассылка: {category.name}',
                    message='',
                    html_message=html_content,
                    from_email=None,
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                )


@shared_task
def send_welcome_email(user_id):
    """Приветственное письмо новому пользователю"""
    from django.contrib.auth.models import User
    user = User.objects.get(id=user_id)

    html_content = render_to_string(
        'email/welcome_email.html',
        {'user': user}
    )

    send_mail(
        subject='Добро пожаловать на News Portal!',
        message='',
        html_message=html_content,
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )