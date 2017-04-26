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
    
    def test_can_start_a_list_and_retrieve_it_later(self):
        
        self.browser.get(self.live_server_url)

        self.assertIn('BusWaiting', self.browser.title, 
                      "title is " + self.browser.title)
        
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('BusWaiting', header_text)
        
        inputbox = self.browser.find_element_by_name('busStop')
        inputbox.send_keys("ท่าน้ำนนท์บุรี")
        inputbox.send_keys(Keys.ENTER)
        
        time.sleep(1)
        
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("ท่าน้ำนนท์บุรี", header_text)
        
        self.check_for_row_in_list_table("97")
            
        table = self.browser.find_element_by_id("97")
        link = table.find_element_by_link_text("report")
        link.click()
        
        time.sleep(1)
        
        linkset = self.browser.find_element_by_tag_name('body')
        backlink = linkset.find_element_by_link_text("back")
        backlink.click()
        
        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        self.browser.get(self.live_server_url)
        
        inputbox = self.browser.find_element_by_name('busStop')
        inputbox.send_keys("โรงเรียนสตรีนนทบุรี")
        inputbox.send_keys(Keys.ENTER)
        
        time.sleep(1)
        
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("โรงเรียนสตรีนนทบุรี", header_text)
        
        timetext = self.browser.find_element_by_id('ท่าน้ำนนท์บุรี_time')
        self.assertNotEqual(timetext, "-")
        
        self.fail('Finish the test!')
        
    def create_object(self):
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

if __name__ == '__main__':
    unittest.main(warnings='ignore')