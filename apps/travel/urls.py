from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main$', views.index),
    url(r'login$', views.login),
    url(r'register$', views.register),
    url(r'travels$', views.home),
    url(r'travels/destination/(?P<trip_id>\d+)', views.display_trip),
    url(r'travels/add', views.add),
    url(r'travels/new', views.new_travel),
    url(r'travels/(?P<trip_id>\d+)', views.add_to_trip)
]