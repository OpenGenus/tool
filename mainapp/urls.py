from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [
url('capitalize/',views.capitalize,name='capitalize'),
url('',views.home,name='home'),
]
