from django.contrib.sitemaps import Sitemap
from mainapp.models import UserProfile,Tag,Tool
from mainapp.urls import urlpatterns as homeUrls
from django.urls import reverse

class ToolSitemap(Sitemap):
    changefreq = "always"
    priority = 0.6

    def items(self):
       return Tool.objects.all()

class UserSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
       return UserProfile.objects.all()

class TagSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
       return Tag.objects.all()


class StaticSitemap(Sitemap):
     priority = 0.6
     changefreq = 'weekly'

     # The below method returns all urls defined in urls.py file
     def items(self):
        mylist = []
        for url in homeUrls:
            print(url.name)
            if url.name is None:
                url.name = "media"
            mylist.append('mainapp:'+url.name) 
        return mylist

     def location(self, item):
         return reverse(item)