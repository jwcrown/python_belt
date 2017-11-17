# DASHBOARD APP LEVEL
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^add$', views.add),
    url(r'^(?P<id>\d+)/delete$', views.delete),
    url(r'^(?P<apt_id>\d+)/edit$', views.edit),
    url(r'^(?P<apt_id>\d+)/update$', views.update),
]