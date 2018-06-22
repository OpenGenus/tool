from django.conf.urls import url
from django.contrib import admin
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
url(r'^t/(?P<tool_name>[^/]+)/$',views.tool,name='tool'),
url(r'^convert_file/$',views.convert_file,name='convert_file'),
url(r'^JPG_To_PNG/$',views.JpgToPng,name='JPG_To_PNG'),
url(r'^$',views.home,name='home'),
url(r'^u/(?P<user_name>[^/]+)/$',views.user_profile,name='user_profile'),
url(r'^tags/(?P<tag_name>[^/]+)/$',views.tags,name='tag'),
url(r'^category/(?P<category_name>[^/]+)/$',views.category,name='category')
]
if settings.DEBUG is True:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
