from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^healthcheck', views.health, name='health'),
    url(r'^stats', views.stats, name='stats'),
    url(r'^admin$', views.admin, name='comadmin'),
    url(r'^admin/updateunits', views.update, name='update'),
    url(r'^thunderdome', views.thunderdome, name='thunderdome')
    )