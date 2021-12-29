from django.conf import settings
from django.db import models


class Blog(models.Model):
    title = models.CharField('Название', max_length=128)
    description = models.TextField('Описание', max_length=512)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField('Заголовок', max_length=64)
    content = models.TextField('Текст', max_length=5120)
    post_time = models.DateTimeField('Время публикации', auto_now_add=True)
    blog = models.ForeignKey(
        'Blog',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    blog = models.ForeignKey(
        'Blog',
        on_delete=models.CASCADE
    )
    subscription_date = models.DateTimeField('Дата подписки', auto_now_add=True)

    def __str__(self):
        return f'Subscription {self.user} on {self.blog}'


class PostReadHistory(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    date_created = models.DateTimeField('Дата прочтения поста', auto_now_add=True)

    def __str__(self):
        return f'{self.post.id}'
