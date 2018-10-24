from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^hacker$', views.hacker),
    url(r'^new$', views.new),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^show/(?P<id>\d+)$', views.show),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^new_job$', views.new_job),
    url(r'^add$', views.add),
    url(r'^update/(?P<id>\d+)$', views.update),
    url(r'^delete$', views.delete),
    url(r'^give_up$', views.give_up)
]