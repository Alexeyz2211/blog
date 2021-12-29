from typing import Any, Dict

from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models
from .tasks import send_email_notice


@receiver(post_save, sender=models.Post)
def on_post_save(instance: models.Post, created: bool, **kwargs: Dict[str, Any]):
    if created:
        users = models.Subscription.objects.filter(blog__post=instance.id)
        users = [u.user for u in users]
        send_email_notice(users)
