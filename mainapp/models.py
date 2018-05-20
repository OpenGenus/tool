from django.db import models

# Create your models here.


class Tool(models.Model):
    tool_name = models.CharField(max_length=30)
    meta_description = models.TextField()
    meta_title = models.CharField(max_length=30)
    long_description = models.TextField()
    short_description = models.TextField()
    author_name = models.CharField(max_length=30)
    editors = models.TextField()
    template_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
