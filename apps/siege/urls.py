from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.manage, name='manage'),
    url(r'^armies$', views.show_armies, name='armies'),
    url(r'^new$', views.create_siege, name='new'),
    url(r'^armies/new$', views.create_army, name='newarmy'),
    url(r'^(?P<siege>\d+)/addarmy$', views.add_army_tosiege, name='add_army'),
    url(r'^(?P<siege>\d+)$', views.edit_siege, name='edit_siege'),
    url(r'^armies/(?P<army>\d+)$', views.save_army, name="update_army"),
    url(r'^(?P<siege>\d+)/armies/(?P<army>\d+)$', views.update_siegearmy, name="update_siegearmy"),
    url(r'^cities$', views.show_cities, name='cities'),
    url(r'^cities/new$', views.create_city, name='newcity'),
    url(r'^cities/(?P<city>\d+)$', views.save_city, name="update_city"),
    url(r'^(?P<siege>\d+)/schedule$', views.schedule, name="schedule"),
    url(r'^myschedule$', views.player_schedule, name="myschedule"),
    )
