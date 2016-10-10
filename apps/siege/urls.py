from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.manage, name='manage'),
    url(r'^dashboard$', views.manage, name='manage'),
    url(r'^armies$', views.show_armies, name='armies'),
    url(r'^new$', views.create_siege, name='new'),
    url(r'^armies/new$', views.create_army, name='newarmy'),
    url(r'^(?P<siege>\d+)/addarmy$', views.add_army, name='add_army'),
    url(r'^(?P<siege>\d+)$', views.edit_siege, name='edit_siege'),
    )
