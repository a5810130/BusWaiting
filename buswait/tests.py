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
        response = self.client.get('/busStop/', data={'busStop': 'somebusstop'})
        self.assertIn(b'somebusstop', response.content)


class BusDetailTest(TestCase):
    
    def test_root_url_resolves_to_index_view(self):
        found = resolve('/bus/')
        self.assertEqual(found.func, busDetail)
        
    def test_usesd_index_template(self):
        response = self.client.get('/bus/')
        self.assertTemplateUsed(response, 'buswait/busDetail.html')
        
    def test_can_save_a_POST_request(self):
        response = self.client.get('/bus/', data={'busNumber': 'somebus'})
        self.assertIn(b'somebus', response.content)


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
        first_busstop = route.busstop_set.create(name="first_busstop")
        second_busstop = route.busstop_set.create(name="second_busstop")
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
        previous_set_of_second = second_saved_busstop.get_previous()
        self.assertEqual(previous_set_of_second.count(), 2)
        self.assertIn(first_saved_busstop, previous_set_of_second)
        
        route2 = Route(bus_number="another route")
        route2.save()
        first_another_busstop = route2.busstop_set.create(name="first_busstop")
        previous_of_first_another = first_another_busstop.get_previous()
        self.assertEqual(previous_of_first_another.count(), 1)