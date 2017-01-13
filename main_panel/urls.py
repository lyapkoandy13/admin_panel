from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^ajax/check/user/', views.check_user, name='check_user'),
    url(r'^bazalt/', views.bazalt, name='bazalt'),
]