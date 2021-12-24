from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.EmailField('Адрес электронной почты', max_length=64, unique=True, null=False)
    first_name = models.CharField('Имя', max_length=64, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'first_name']
