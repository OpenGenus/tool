from django.conf.urls import url
from django.contrib import admin
from . import tool_views, views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
url(r'^convert_image/$',tool_views.convert_image,name='convert_image'),
url(r'^convert_file/$',tool_views.convert_file,name='convert_file'),
url(r'^minify/$', tool_views.show_minified_js,name = 'show_minified_js'),
url(r'^minify_file/$', tool_views.download_minified_file, name = 'download_minified_JS'),
url(r'^download/$', tool_views.download_file,name = 'download_minified_file'),
url(r'^jpg_to_png/$',tool_views.jpg_to_png,name='jpg_to_png'),
url(r'^about_sample_file/(?P<format>[\w]+)/$', tool_views.about_sample_file,name='about_sample_file'),
url(r'^download_sample_file/(?P<format>[^/]+)/$', tool_views.download_sample_file, name = 'download_sample_file'),
url(r'^website_status/$',tool_views.website_status,name='website_status'),
url(r'^detect_lang/$',tool_views.detect_lang,name='detect_lang'),
url(r'^generatepdf/$',tool_views.generate_pdf,name='generate_pdf'),
url(r'^delete_generated_pdf/(?P<path>[^/]+)/$',tool_views.delete_generated_pdf,name='delete_generated_pdf'),
url(r'^download_generated_pdf/(?P<path>[^/]+)/$',tool_views.download_generated_pdf,name='download_generated_pdf'),
url(r'^view_generated_pdf/(?P<path>[^/]+)/$',tool_views.view_generated_pdf,name='view_generated_pdf'),

]

if settings.DEBUG is True:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, name='staticfiles')
