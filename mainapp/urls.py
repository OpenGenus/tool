from django.conf.urls import url
from django.contrib import admin
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
url(r'^$',views.home,name='home'),
url(r'^convert_file/$',views.convert_file,name='convert_file'),
url(r'^minify/$', views.show_minified_js,name = 'show_minified_js'),
url(r'^minify_file/$', views.download_minified_file, name = 'download_minified_JS'),
url(r'^download/$', views.download_file,name = 'download_minified_file'),
url(r'^JPG_To_PNG/$',views.JpgToPng,name='JPG_To_PNG'),
]