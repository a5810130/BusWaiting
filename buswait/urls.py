from django.conf.urls import url, include
from django.conf import settings
from django.views.generic import TemplateView

from . import views

app_name = 'buswait'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^busStop/$', views.busStopDetail, name='busStopDetail'),
    url(r'^bus/$', views.busDetail, name='busDetail'),
    url(r'^about/$', TemplateView.as_view(template_name='buswait/about.html'), name='about'),
    url(r'^report/(?P<busStop_id>[0-9]+)/$', views.report_bus, name='report_bus'),
	url(r'^register/$', views.register, name='register'),
	url('^', include('django.contrib.auth.urls')),
	url(r'^logout_success/$', views.logout_success, name='logout_success'),
	url(r'^set_favorite_busstop/(?P<busstop>[^\n]+)/$', 
	views.set_favorite_busstop, name='set_favorite_busstop'),
	url(r'^set_favorite_bus/(?P<bus_id>[0-9]+)/$', views.set_favorite_bus, name='set_favorite_bus'),
]