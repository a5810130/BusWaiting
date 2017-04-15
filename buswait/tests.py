from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from buswait.views import *
from buswait.models import *


class IndexTest(TestCase):
    
    def test_root_url_resolves_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_index_returns_correct_html(self):
        request = HttpRequest()  
        response = index(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>BusWaiting App</title>', response.content)
        self.assertIn(b'<h1>BusWaiting App</h1>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))

class RouteModelTest(TestCase):
    
    def test_saving_and_retrieving_items(self):
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