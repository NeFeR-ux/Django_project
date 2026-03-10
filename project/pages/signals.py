from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.contrib.auth.signals import user_logged_in

@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    """Автоматически добавляет нового пользователя в группу common"""
    if created:
        common_group, _ = Group.objects.get_or_create(name='common')
        instance.groups.add(common_group)