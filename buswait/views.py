from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.urls import reverse
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from buswait.models import *

def register(request):
	if request.method == 'POST':
		data = request.POST
		form = UserCreationForm(data)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=password)
			user.save()
			return redirect(reverse('buswait:login'))
	else:
		form = UserCreationForm()	
	return render(request, 'registration/register.html', {'form': form})
	
# def login(request):
	# form = AuthenticationForm()	
	# if request.method == 'POST':
		# username = request.POST['username']
		# password = request.POST['password']
		# user = authenticate(request, username=username, password=password)
		# if user is not None:
			# login(request, user)
			# return redirect(reverse('buswait:home'))
	# return render(request, 'registration/login.html', {'form': form})
		
def logout_success(request):
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def index(request):
	busStop_set = BusStop.objects.values('name').distinct()
	bus_set = Route.objects.values('bus_number').distinct()
	data = {'busStop_set': busStop_set, 'bus_set': bus_set}
	return render(request, 'buswait/index.html', data)

	
def busStopDetail(request):
	busStop_datalist = BusStop.objects.values('name').distinct()
	busStopName = ''
	busStop_set = set()
	filter = ''
	
	try:
		busStopName = request.GET['busStop']
		filter = request.GET['filter']
		busStop_set = BusStop.objects.filter(name=busStopName)
		if (filter != ""):
			temp = []
			for busStop in busStop_set:
				if (busStop.busFilter(filter) == True):
					temp.append(busStop)
			busStop_set = temp		
	except:
		pass
		
	context = {	'busStopName': busStopName, 'busStop_set': busStop_set, 
				'filter': filter, 'busStop_datalist': busStop_datalist}
	return render(request, 'buswait/busStopDetail.html', context)


def busDetail(request):
	busNumber = ''
	busStop_set = set()

	try:
		busNumber = request.GET['busNumber']
		bus = Route.objects.filter(bus_number=busNumber).first()
		busStop_set = bus.busstop_set.all()
	except:
		pass

	context = {'busNumber': busNumber, 'busStop_set': busStop_set}
	return render(request, 'buswait/busDetail.html', context)


def report_bus(request, busStop_id):
	busStop = get_object_or_404(BusStop, id=busStop_id)
	busStop.time = timezone.now()
	busStop.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))