from django.db import models

# Create your models here.


class Tool(models.Model):
    tool_name = models.CharField(max_length=30)
    url_endpoint = models.CharField(max_length=30,blank=True)
    meta_description = models.TextField(blank=True)
    meta_title = models.CharField(max_length=30,blank=True  )
    long_description = models.TextField(blank=True)
    short_description = models.TextField(blank=True)
    author_name = models.CharField(max_length=30,  blank=True)
    editors = models.TextField(blank=True)
    template_name = models.CharField(max_length=30,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tool_name
