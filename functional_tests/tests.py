from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        
        self.browser.get(self.live_server_url)

        self.assertIn('BusWaiting', self.browser.title, "title is " + self.browser.title)
        
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('BusWaiting', header_text)
        
        dropdownbox = self.browser.find_element_by_id('busStop')
        dropdownbox.select_by_visible_text('พระจอมเกล้าพระนครเหนือ')
        
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')