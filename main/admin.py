from django.contrib import admin
from . import models

admin.site.register(models.Blog)
admin.site.register(models.Post)
admin.site.register(models.Subscription)
admin.site.register(models.PostReadHistory)
