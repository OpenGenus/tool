from django.conf.urls import url
from django.contrib import admin
from . import tool_views, views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
url(r'^convert_file/$',tool_views.convert_file,name='convert_file'),
url(r'^minify/$', tool_views.show_minified_js,name = 'show_minified_js'),
url(r'^minify_file/$', tool_views.download_minified_file, name = 'download_minified_JS'),
url(r'^download/$', tool_views.download_file,name = 'download_minified_file'),
url(r'^jpg_to_png/$',tool_views.jpg_to_png,name='jpg_to_png'),
url(r'^about_sample_file/(?P<format>[\w]+)/$', tool_views.about_sample_file,name='about_sample_file'),
url(r'^download_sample_file/(?P<format>[^/]+)/$', tool_views.download_sample_file, name = 'download_sample_file'),
]

if settings.DEBUG is True:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, name='staticfiles')
