from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    discourse = models.URLField(null=True, blank=True)
    about = models.TextField()
    profilepic = models.FileField(blank=True,null=True,upload_to='profile_pic')
    github =  models.URLField(null=True, blank=True)
    website = models.URLField(null=True,blank=True )

    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


class Tag(models.Model):
    tag = models.CharField(max_length=30)

    def __str__(self):
        return self.tag



class Tool(models.Model):
    tool_name = models.CharField(max_length=30)
    url_endpoint = models.CharField(max_length=30,blank=True)
    meta_description = models.TextField(blank=True)
    meta_title = models.CharField(max_length=30,blank=True  )
    long_description = models.TextField(blank=True)
    short_description = models.TextField(blank=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='author_tool_set')
    editors = models.ManyToManyField(UserProfile, related_name='editors_tool_set',blank=True)
    tags = models.ManyToManyField(Tag,blank=True)
    template_name = models.CharField(max_length=30,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tool_name
