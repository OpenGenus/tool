from django.conf.urls import url
from django.contrib import admin
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
url(r'^t/(?P<tool_name>[^/]+)/$',views.tool,name='tool'),
url(r'^$',views.home,name='home'),
url(r'^u/(?P<user_name>[^/]+)/$',views.user_profile,name='user_name'),
]
if settings.DEBUG is True:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
