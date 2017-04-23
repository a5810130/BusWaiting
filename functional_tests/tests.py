from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from buswait.models import *
from django.utils import timezone

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.create_object()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, bus_number):
        table = self.browser.find_element_by_id('bus_table')
        columns = table.find_elements_by_tag_name('td')
        self.assertIn(bus_number, [column.text for column in columns])
        
    def choose_busStop_view_report_and_back(self, busStop, views, report=None):
        inputbox = self.browser.find_element_by_name('busStop')
        inputbox.send_keys(busStop)
        inputbox.send_keys(Keys.ENTER)
        
        time.sleep(1)
        
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn(busStop, header_text)
        
        for view in views:
            self.check_for_row_in_list_table(view)
            
        if (report != None):
            table = self.browser.find_element_by_id(report)
            link = table.find_element_by_link_text("report")
            link.click()
        
            time.sleep(1)
        
        linkset = self.browser.find_element_by_tag_name('body')
        backlink = linkset.find_element_by_link_text("back")
        backlink.click()
        
        time.sleep(1)
    
    def test_can_start_a_list_and_retrieve_it_later(self):
        
        print(Route.objects.all())
        print(BusStop.objects.values(
            'name').distinct().filter(
            bus_terminus=False))
        
        self.browser.get(self.live_server_url)

        self.assertIn('BusWaiting', self.browser.title, 
                      "title is " + self.browser.title)
        
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('BusWaiting', header_text)
        
        self.choose_busStop_view_report_and_back(
            "โรงเรียนสตรีนนทบุรี",
            ["97"], 
            "97")
        self.choose_busStop_view_report_and_back(
            "อนุสาวรีย์ชัยสมรภูมิ", 
            ["97","โรงเรียนสตรีนนทบุรี"])
        self.choose_busStop_view_report_and_back(
            "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ", 
            ["97","โรงเรียนสตรีนนทบุรี"],
            "97")
        self.choose_busStop_view_report_and_back(
            "อนุสาวรีย์ชัยสมรภูมิ", 
            ["97","มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ"], 
            "97")
        self.choose_busStop_view_report_and_back(
            "ท่าน้ำนนท์บุรี", 
            ["97"], 
            "97")
        
        self.choose_busStop_view_report_and_back(
            "ท่าน้ำนนท์บุรี",
            ["203"], 
            "203")
        self.choose_busStop_view_report_and_back(
            "โรงเรียนสตรีนนทบุรี",
            ["203","ท่าน้ำนนท์บุรี"])
        self.choose_busStop_view_report_and_back(
            "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ",
            ["203","ท่าน้ำนนท์บุรี"],
            "203")
        self.choose_busStop_view_report_and_back(
            "โรงเรียนสตรีนนทบุรี",
            ["203","-"])
        
        self.fail('Finish the test!')
        
    def create_object(self):
        r203 = Route(bus_number="203")
        r203.save()
        r203.busstop_set.create(name="ท่าอิฐ", bus_terminus=True)
        r203.busstop_set.create(name="ท่าน้ำนนท์บุรี", bus_terminus=False)
        r203.busstop_set.create(name="โรงเรียนสตรีนนทบุรี", bus_terminus=False)
        r203.busstop_set.create(name="มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ", bus_terminus=False)
        r203.busstop_set.create(name="โรงพยาบาลยันฮี", bus_terminus=False)
        r203.busstop_set.create(name="สนามหลวง", bus_terminus=True)
        r203.save()
        r97 = Route(bus_number="97")
        r97.save()
        r97.busstop_set.create(name="กระทรวงสาธารณสุข", bus_terminus=True)
        r97.busstop_set.create(name="ท่าน้ำนนท์บุรี", bus_terminus=False)
        r97.busstop_set.create(name="โรงเรียนสตรีนนทบุรี", bus_terminus=False)
        r97.busstop_set.create(name="มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ", bus_terminus=False)
        r97.busstop_set.create(name="อนุสาวรีย์ชัยสมรภูมิ", bus_terminus=False)
        r97.busstop_set.create(name="โรงพยาบาลสงฆ์", bus_terminus=True)
        r97.save()

if __name__ == '__main__':
    unittest.main(warnings='ignore')