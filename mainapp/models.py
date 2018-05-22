from django.db import models

# Create your models here.
class Tag(models.Model):
    tag = models.CharField(max_length=30)

class Author(models.Model):
    name = models.CharField(max_length=30)
    website =  models.URLField(max_length=100)
    discourse = models.URLField(max_length=100)
    details = models.TextField()

class Tool(models.Model):
    tool_name = models.CharField(max_length=30)
    url_endpoint = models.CharField(max_length=30,blank=True)
    meta_description = models.TextField(blank=True)
    meta_title = models.CharField(max_length=30,blank=True  )
    long_description = models.TextField(blank=True)
    short_description = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE,related_name='author')
    editors = models.ManyToManyField(Author, related_name='editors',blank=True)
    tags = models.ManyToManyField(Tag,blank=True)
    template_name = models.CharField(max_length=30,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tool_name
