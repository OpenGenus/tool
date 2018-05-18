from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [
url(r'^t/(?P<tool_name>[^/]+)/$',views.tool,name='tool'),
url(r'^$',views.home,name='home'),
]
