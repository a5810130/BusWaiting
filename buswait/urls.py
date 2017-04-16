from django.conf.urls import url 
from django.conf import settings

from . import views

app_name = 'buswait'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^busStop/$', views.busStopDetail, name='busStopDetail'),
]