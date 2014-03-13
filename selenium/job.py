import unittest
import os
import string
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

class Beaker_Jobs(unittest.TestCase):
        def setUp(self):
                profile = webdriver.FirefoxProfile('./firefox/autouser2')
                self.driver = webdriver.Firefox(profile)
                driver = self.driver
                driver.get("https://beaker-devel.app.eng.bos.redhat.com/")
                self.assertIn("Systems", driver.title)

        def submit_job(self):
                driver = self.driver
                driver.get("https://beaker-devel.app.eng.bos.redhat.com/jobs/new")
                self.assertIn("New Job", driver.title)

                #click submit button
                driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
                self.assertIn("Clone Job", driver.title)

                #input demo.xml in the text file
                job_xml_input=driver.find_element_by_name("textxml")
                job_xml_file=open('./selenium/demo.xml')
                try:
                        job_xml_content=job_xml_file.read()
                finally:
                        job_xml_file.close()
                job_xml_input.send_keys(job_xml_content)

                #click button "Queue"
                driver.find_element_by_xpath("//button[@class='btn btn-primary btn-block']").click()

                #check the new job id
                driver.implicitly_wait(30)
                self.assertIn("Success! job id:", driver.page_source)

                #get job id
                job_string=driver.find_element_by_xpath("//div[@class='alert flash']").text
                p=re.compile(r': ')
                job_id=p.split(job_string)[1]
                return job_id

        def cancel_job(self, job_id):
                driver=self.driver
                driver.get("https://beaker-devel.app.eng.bos.redhat.com/jobs/cancel?id=" + job_id)
                self.assertIn("Cancel Job", driver.title)
                self.assertIn(job_id, driver.title)
                driver.find_element_by_id("cancel_job_msg").send_keys(job_id)
                driver.find_element_by_xpath("//input[@class='submitbutton']").click()
                self.assertIn("Successfully cancelled job", driver.page_source)

	def clone_job(self, job_id):
                driver=self.driver
                driver.get("https://beaker-devel.app.eng.bos.redhat.com/jobs/clone?id=" + job_id)
                driver.find_element_by_xpath("//button[@class='btn btn-primary btn-block']").click()
                #check the new job id
                driver.implicitly_wait(30)
                self.assertIn("Success! job id:", driver.page_source)
                #get job id
                job_string=driver.find_element_by_xpath("//div[@class='alert flash']").text
                p=re.compile(r': ')
                job_id=p.split(job_string)[1]
                return job_id


	def test_cancel_job(self):
		#driver=self.driver
		#driver.get("https://beaker-devel.app.eng.bos.redhat.com/jobs/mine")
		#self.assertIn("My Jobs",driver.title)
		
		#submit a job
		job_id=self.submit_job()
		self.cancel_job(job_id)

		#cancle a completed job
		#driver.find_element_by_xpath("//div[@class='btn-group']/button[@value='Status-is-Completed']").click()
		#job_id=driver.find_element_by_xpath("//tbody/tr[1]/td[1]").text
		#driver.find_element_by_xpath("//tbody/tr[1]/td[8]/div/a[2]").click()
		#self.assertIn("Cancel Job", driver.title)
		#self.assertIn(job_id, driver.title)
		#driver.find_element_by_id("cancel_job_msg").send_keys(job_id)
		#driver.find_element_by_xpath("//input[@class='submitbutton']").click()
		#self.assertIn("Successfully cancelled job", driver.page_source)

	def tearDown(self):
		pass
		#self.driver.close()

suite = unittest.TestLoader().loadTestsFromTestCase(Beaker_Jobs)
unittest.TextTestRunner(verbosity=2).run(suite)

