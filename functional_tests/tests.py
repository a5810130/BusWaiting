from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from buswait.models import *
from django.utils import timezone

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.create_object()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, bus_number):
        table = self.browser.find_element_by_id('bus_table')
        columns = table.find_elements_by_tag_name('td')
        self.assertIn(bus_number, [column.text for column in columns])
    
    def test_can_access_detail_and_report(self):
		# สมปองอยู่ที่ป้ายรถเมย์
		# เขาเข้าเว็บ buswaiting
        self.browser.get(self.live_server_url)
	
		# เขาพบกับเว็บ buswaitng
        self.assertIn('BusWaiting', self.browser.title, 
                      "title is " + self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('BusWaiting', header_text)
        
		# เขากรอก"ท่าน้ำนนท์บุรี"ลงในช่อง busstop
        inputbox = self.browser.find_element_by_name('busStop')
        inputbox.send_keys("ท่าน้ำนนท์บุรี")
        inputbox.send_keys(Keys.ENTER)
        
        time.sleep(1)
        
		# เขาพบกับหน้าแสดงของมูลของป้ายท่าน้ำนนท์บุรี
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("ท่าน้ำนนท์บุรี", header_text)
        
		# เขาพบสาย 97 ผ่านพอดี จึงมองหาสาย 97 ในตารางแสดงข้อมูล 
        self.check_for_row_in_list_table("97")
        # เข้ากด report สาย 97 ว่ามีรถผ่าน
        table = self.browser.find_element_by_id("97")
        link = table.find_element_by_link_text("report")
        link.click()
        
        time.sleep(1)
        
		# เสร็จแล้วเขาจึงกด back และปิดเว็บ
        linkset = self.browser.find_element_by_tag_name('body')
        backlink = linkset.find_element_by_link_text("back")
        backlink.click()
        
        self.browser.quit()
		
		# สมหมายมาถึงป้ายโรงเรียนสตรีนนทบุรี
		# เขาได้เขามาที่เว็บ buswaiting
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        
		# เขากรอก"โรงเรียนสตรีนนทบุรี"ลงในช่อง busstop
        inputbox = self.browser.find_element_by_name('busStop')
        inputbox.send_keys("โรงเรียนสตรีนนทบุรี")
        inputbox.send_keys(Keys.ENTER)
        
        time.sleep(1)
        
		# เขาพบกับหน้าแสดงข้อมูล
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("โรงเรียนสตรีนนทบุรี", header_text)
        
        # เขามองหาข้อมูลของสาย 97 และพบมีเวลาถูก report ที่ป้ายท่าน้ำนนท์ทบุรีไว้แล้ว
        table = self.browser.find_element_by_id("97")
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