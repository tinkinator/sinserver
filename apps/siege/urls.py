from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.manage, name='manage'),
    url(r'^dashboard$', views.manage, name='manage'),
    url(r'^armies$', views.armies, name='armies'),
    url(r'^new$', views.create_siege, name='new'),
    url(r'^(?P<siege>\d+)', views.edit_siege, name='edit_siege'),
    )
