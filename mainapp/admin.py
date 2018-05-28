from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Tool)
admin.site.register(models.UserProfile)
admin.site.register(models.Tag)
