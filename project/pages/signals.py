from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.contrib.auth.signals import user_logged_in
from .tasks import send_welcome_email
from .tasks import send_new_post_notification
from .models import Post


@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    if created:
        common_group, _ = Group.objects.get_or_create(name='common')
        instance.groups.add(common_group)
        # Отправка приветственного письма
        send_welcome_email.delay(instance.id)

@receiver(post_save, sender=Post)
def notify_subscribers_about_new_post(sender, instance, created, **kwargs):
    if created:
        send_new_post_notification.delay(instance.id)