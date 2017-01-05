from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^create_user', views.create_user, name="create_user"),
	url(r'^send_message', views.send_message, name="send_message"),
	url(r'^delete_user', views.delete_user, name="delete_user"),
	url(r'^grant_access', views.grant_access, name="grant_access"),
	url(r'^deny_access', views.deny_access, name="deny_access"),
]