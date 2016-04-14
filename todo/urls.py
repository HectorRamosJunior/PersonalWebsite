from django.conf.urls import url, include

from . import views

urlpatterns = [
	#todo/
	url(r'^$', views.index, name='index'),

	#todo/register/ is the example format for the below
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    #url(r'^create_task/$', views.create_task, name='create_task'),

	#todo/<user>
	url(r'^(?P<username>\w+)/$', views.user_profile, name='user_profile'),
	#todo/user/task/
	#url(r'^(?P<account_name>\w+)/(?P<task_id>[0-9]+)/$', views.task, name='task'),	
]
