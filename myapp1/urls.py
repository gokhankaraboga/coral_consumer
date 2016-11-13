from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'},
        name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'},
        name='logout'),
    url(r'^$', auth_views.login, {'template_name': 'login.html'},
        name='login'),
    url(r'^homepage/$', views.homepage, name='homepage'),
    url(r'^destination_search/$', views.destination_search,
        name='destination_search'),
    url(r'^single_hotel_search/$', views.single_hotel_search,
        name='single_hotel_search'),
    url(r'^booking_page/$', views.booking_page,
        name='booking_page'),
]
