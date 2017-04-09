from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/send_mail/$', views.ajax_send_mail, name='ajax_send_mail'),
] 