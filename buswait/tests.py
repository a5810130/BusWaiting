from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from buswait.views import *


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
        
    def test_index_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['busStop'] = 'location'

        response = home_page(request)

        self.assertIn('location', response.content.decode())