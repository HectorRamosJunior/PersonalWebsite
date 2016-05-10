"""MySite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), 
    url(r'^login/$', views.user_login_or_register, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^make_twoot/$', views.make_twoot, name='make_twoot'),
    url(r'^settings/$', views.profile_settings, name='profile_settings'),
    url(r'^notifications/$', views.profile_notifications, name='profile_notifications'),
    url(r'^favorite_twoot/$', views.favorite_twoot, name='favorite_twoot'),
    url(r'^retwoot_twoot/$', views.retwoot_twoot, name='retwoot_twoot'),
    url(r'^delete_twoot/$', views.delete_twoot, name='delete_twoot'),
    url(r'^profile_list/$', views.profile_list, name='profile_list'),
    url(r'^twoot/(?P<twoot_pk>\w+)/$', views.view_twoot, name='view_twoot'),
    url(r'^user/(?P<username>.+)/$', views.twotter_profile, name='twotter_profile'),
    url(r'^search/(?P<search>.+)/$', views.twotter_search, name='twotter_search'), 
    url(r'^search/$', views.twotter_search, name='twotter_search'),
    url(r'^', views.redirect_to_index, name='redirect_to_index'),  
]
