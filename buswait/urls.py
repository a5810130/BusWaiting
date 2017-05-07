from django.conf.urls import url 
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
]