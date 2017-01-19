from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.log_in, name='login'),
    url(r'^logout$', views.log_out, name='logout'),
    url(r'^account$', views.account, name='account'),
    url(r'^account/name', views.playername),
    url(r'^account/checkpassword', views.checkpassword),
    url(r'^account/password', views.password),
    url(r'^account/apikey', views.apikey),
    url(r'^account/email', views.email),

    )
