from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.log_in, name='login'),
    url(r'^logout$', views.log_out, name='logout'),
    )
