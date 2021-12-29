from typing import Any, Dict

from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models
from main.models import Blog


@receiver(post_save, sender=models.User)
def on_user_save(instance: models.User, created: bool, **kwargs: Dict[str, Any]):
    if created:
        Blog.objects.create(
            title=f'{instance.first_name}\'s blog',
            user=instance
        )

