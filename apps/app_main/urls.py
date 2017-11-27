from django.conf.urls import url
from django.contrib import admin
from .import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^create$', views.create),
    url(r'^users/(?P<id>\d+)/$', views.display),
    url(r'^favorite/(?P<id>\d+)/$', views.favorite),
    url(r'^remove/(?P<id>\d+)/$', views.remove),
    url(r'^logout$', views.logout),
]