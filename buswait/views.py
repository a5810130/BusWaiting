from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone 

from buswait.models import *

def index(request):
    busStop_set = BusStop.objects.values('name').distinct().filter(bus_terminus=False)
    data = {'busStop_set':busStop_set,}
    return render(request, 'buswait/index.html', data)

def busStopDetail(request):
    busStopName=""
    bus_location_set = set()
    
    if request.method == 'POST':
        busStopName = request.POST['busStop']
        try:
            busStop_set = BusStop.objects.filter(name=busStopName)
            print(busStop_set)
            for busStop in busStop_set:
                bus_coming = busStop.find_bus_coming()
                print(bus_coming)
                bus_location_set.add(bus_coming)
                print(bus_location_set)
        except :
            pass
        
    context = {'busStopName':busStopName, 'bus_location_set':bus_location_set}
    return render(request, 'buswait/busStopDetail.html', context)

def report_bus(request, busStop_id):
    busStop = get_object_or_404(BusStop, id=busStop_id)
    time = timezone.now()
    busStop.add_time(time)