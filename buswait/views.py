from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone 
from django.urls import reverse

from buswait.models import *

def index(request):
    busStop_set = BusStop.objects.values(
        'name').distinct().filter(
            bus_terminus=False)
    data = {'busStop_set':busStop_set,}
    return render(request, 'buswait/index.html', data)

def busStopDetail(request):
    busStopName = ""
    bus_location_set = set()
    
    if request.method == 'GET':
        busStopName = request.GET['busStop']
        try:
            busStop_set = BusStop.objects.filter(name=busStopName)
            for busStop in busStop_set:
                bus_location_set.add(busStop)
        except :
            pass
        
    context = {'busStopName':busStopName, 
               'bus_location_set':bus_location_set}
    return render(request, 'buswait/busStopDetail.html', context)

def report_bus(request, busStop_id):
    busStop = get_object_or_404(BusStop, id=busStop_id)
    time = timezone.now()
    busStop.add_time(time)
    urlredirect = reverse('buswait:busStopDetail')+'?busStop='+busStop.name
    return HttpResponseRedirect(urlredirect)