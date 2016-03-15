"""railroads URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from trains_schedule.views import CityList,CityDetail

'''
usage:
http DELETE http://127.0.0.1:8000/api/city/18/
http --form POST http://127.0.0.1:8000/api/city/ city_name="vova"

'''

urlpatterns = [
    url(r'^schedule/', include('trains_schedule.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.main, name='main'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^api/city/$',CityList.as_view()),
    url(r'^api/city/(?P<pk>[0-9]+)/$', CityDetail.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)