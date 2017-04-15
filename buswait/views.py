from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse

from buswait.models import *

def index(request):
    busStop_set = BusStop.objects.values('name').distinct()
    data = {'busstop':busStop_set,}
    return render(request, 'buswait/index.html', data)
