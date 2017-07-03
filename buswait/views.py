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
		
def logout_success(request):
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def index(request):
	busStop_set = BusStop.objects.values('name').distinct()
	bus_set = Route.objects.values('bus_number').distinct()
	data = {'busStop_set': busStop_set, 'bus_set': bus_set}
	if request.user.is_authenticated:
		user = request.user
		favorite_busstop = FavoriteBusStop.objects.filter(user=user)
		favorite_bus = FavoriteBus.objects.filter(user=user)
		data['favorite_busstop'] = favorite_busstop
		data['favorite_bus'] = favorite_bus
	return render(request, 'buswait/index.html', data)

	
def busStopDetail(request):
	# create default context
	busStop_datalist = BusStop.objects.values('name').distinct()
	busStopName = ''
	busStop_set = set()
	filter = ''
	favorite = False
	context = {	'busStopName': busStopName, 'busStop_set': busStop_set, 
				'filter': filter, 'busStop_datalist': busStop_datalist,
				'favorite': favorite}
	try:
		busStopName = request.GET['busStop']
		filter = request.GET['filter']
		busStop_set = BusStop.objects.filter(name=busStopName)
		
		if (filter != ""):	# check filter
			temp = []
			for busStop in busStop_set:
				if (busStop.busFilter(filter) == True):
					temp.append(busStop)
			busStop_set = temp	
			
		context['busStopName'] = busStopName
		context['busStop_set'] = busStop_set
		context['filter'] = filter
		context['busStop_datalist'] = busStop_datalist
		
		if request.user.is_authenticated:	# check favorite
			user = request.user
			favorite = FavoriteBusStop.objects.filter(user=user, busstop=busStopName)
			context['favorite'] = favorite.exists()
	except:
		pass
		
	return render(request, 'buswait/busStopDetail.html', context)


def busDetail(request):
	busNumber = ''
	busStop_set = set()
	favorite = False
	context = {'busNumber': busNumber, 'busStop_set': busStop_set,
	'favorite': favorite}
	
	try:
		busNumber = request.GET['busNumber']
		bus = Route.objects.filter(bus_number=busNumber).first()
		busStop_set = bus.busstop_set.all()
		context['busNumber'] = bus
		context['busStop_set'] = busStop_set
		if request.user.is_authenticated:	# check favorite
			user = request.user
			favorite = FavoriteBus.objects.filter(user=user, bus=bus)
			context['favorite'] = favorite.exists()
	except:
		pass

	return render(request, 'buswait/busDetail.html', context)


def report_bus(request, busStop_id):
	busStop = get_object_or_404(BusStop, id=busStop_id)
	busStop.time = timezone.now()
	busStop.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def set_favorite_busstop(request, busstop):
	user = request.user
	favorite = FavoriteBusStop.objects.filter(user=user, busstop=busstop)
	if favorite.exists():
		favorite.delete()
	else:
		favorite = FavoriteBusStop(user=user, busstop=busstop)
		favorite.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	
@login_required
def set_favorite_bus(request, bus_id):
	user = request.user
	bus = get_object_or_404(Route, id=bus_id)
	favorite = FavoriteBus.objects.filter(user=user, bus=bus)
	if favorite.exists():
		favorite.delete()
	else:
		favorite = FavoriteBus(user=user, bus=bus)
		favorite.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	
def create_object():
	r203 = Route(bus_number="203")
	r203.save()
	r203.busstop_set.create(name="ท่าอิฐ")
	r203.busstop_set.create(name="ท่าน้ำนนท์บุรี")
	r203.busstop_set.create(name="โรงเรียนสตรีนนทบุรี")
	r203.busstop_set.create(name="มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ")
	r203.busstop_set.create(name="โรงพยาบาลยันฮี")
	r203.busstop_set.create(name="สนามหลวง")
	r203.save()
	r97 = Route(bus_number="97")
	r97.save()
	r97.busstop_set.create(name="กระทรวงสาธารณสุข")
	r97.busstop_set.create(name="ท่าน้ำนนท์บุรี")
	r97.busstop_set.create(name="โรงเรียนสตรีนนทบุรี")
	r97.busstop_set.create(name="มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ")
	r97.busstop_set.create(name="อนุสาวรีย์ชัยสมรภูมิ")
	r97.busstop_set.create(name="โรงพยาบาลสงฆ์")
	r97.save()