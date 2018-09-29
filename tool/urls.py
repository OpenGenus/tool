"""tool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from .sitemaps import *
from django.contrib.sitemaps.views import sitemap
from mainapp import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView


sitemaps = {
   'Tools': ToolSitemap(),
   'Users': UserSitemap(),
   'Tags' : TagSitemap(),
   'static': StaticSitemap(),
}

urlpatterns = [
    url(r'^admin/', admin.site.urls, name = 'admin_URLs'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^u/(?P<user_name>[^/]+)/$',views.user_profile,name='user_profile'),
    url(r'^t/(?P<tool_name>[^/]+)/$',views.tool,name='tool'),
    url(r'^timeline/$',views.timeline,name='timeline'),
    url(r'^tags/(?P<tag_name>[^/]+)/$',views.tags,name='tag'),
    url(r'^category/(?P<category_name>[^/]+)/$',views.category,name='category'),
    url(r'^contribute/$',TemplateView.as_view(template_name="general/contribution.html"),name='home'),
    url(r'^',include(('mainapp.urls','mainapp'),namespace = 'mainapp_URLs')),
    url(r'^$',views.home,name='home'),
    
    url(r'^discourse_login/$',views.discourse_login,name='discourse_login'),
    url(r'^discourse_login_success/$',views.discourse_login_success,name='discourse_login_success'),
    
    url(r'^logout/$',views.logout,name='logout'),
   
    
]

if settings.DEBUG is True:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
