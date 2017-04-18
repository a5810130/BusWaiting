from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.utils import timezone
import datetime

from buswait.views import *
from buswait.models import *


class IndexTest(TestCase):
    
    def test_root_url_resolves_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)
        
    def test_usesd_index_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'buswait/index.html')


class BusStopDetailTest(TestCase):
    
    def test_root_url_resolves_to_index_view(self):
        found = resolve('/busStop/')
        self.assertEqual(found.func, busStopDetail)
        
    def test_usesd_index_template(self):
        response = self.client.get('/busStop/')
        self.assertTemplateUsed(response, 'buswait/busStopDetail.html')
        
    def test_can_save_a_POST_request(self):
        response = self.client.post('/busStop/', data={'busStop': 'some bus stop'})
        self.assertIn(b'some bus stop', response.content)


class RouteModelTest(TestCase):
    
    def test_saving_and_retrieving(self):
        first_route = Route(bus_number="first_route")
        first_route.save()

        second_route = Route(bus_number="second_route")
        second_route.save()

        saved_route = Route.objects.all()
        self.assertEqual(saved_route.count(), 2)

        first_saved_route = saved_route[0]
        second_saved_route = saved_route[1]
        self.assertEqual(first_saved_route.bus_number, "first_route")
        self.assertEqual(second_saved_route.bus_number, "second_route")
        
        
class BusStopModelTest(TestCase):
    
    def create_model(self):
        route = Route(bus_number="some route")
        route.save()
        first_busstop = route.busstop_set.create(name="first_busstop", bus_terminus=True)
        second_busstop = route.busstop_set.create(name="second_busstop", bus_terminus=False)
        route.save()
        return route
    
    def test_saving_and_retrieving(self):
        route = self.create_model()
        
        saved_busstop = route.busstop_set.all()
        self.assertEqual(saved_busstop.count(), 2)
        
        first_saved_busstop = saved_busstop[0]
        second_saved_busstop = saved_busstop[1]
        self.assertEqual(first_saved_busstop.name, "first_busstop")
        self.assertEqual(second_saved_busstop.name, "second_busstop")
        
    def test_get_previous_method(self):
        route = self.create_model()
        
        saved_busstop = route.busstop_set.all()
        first_saved_busstop = saved_busstop[0]
        second_saved_busstop = saved_busstop[1]
        previous_of_second = second_saved_busstop.previous()
        self.assertEqual(first_saved_busstop, previous_of_second)
        
        route2 = Route(bus_number="another route")
        route2.save()
        first_another_busstop = route2.busstop_set.create(name="first_busstop", bus_terminus=True)
        previous_of_first_another = first_another_busstop.previous()
        self.assertEqual(previous_of_first_another, None)
        
class PassedTimeModelTest(TestCase):
    
    def test_saving_and_retrieving(self):
        route = Route(bus_number="some route")
        route.save()
        busstop = route.busstop_set.create(name="some_busstop", bus_terminus=True)
        time = timezone.now()
        first_passed = busstop.passedtime_set.create(time=time)
        second_passed = busstop.passedtime_set.create(time=time+datetime.timedelta(days=1))

        saved_time = busstop.passedtime_set.all()
        self.assertEqual(saved_time.count(), 2)
        
        first_saved_time = saved_time[0]
        second_saved_time = saved_time[1]
        self.assertEqual(first_saved_time.time, second_saved_time.time-datetime.timedelta(days=1))
    