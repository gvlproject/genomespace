"""
Module Created on 10/05/2015

@author: Regina Zhang

Last Modification: 23/07/2015

@description:
	module for testing getting DOI for publishing the file/data

"""
from genome_space_test import GenomeSpaceTest as GST
from abc import ABCMeta
from constants import *
import unittest
from selenium.webdriver.support import expected_conditions as EC
import unicodedata

class FilePublish(GST):

	__metaclass__ = ABCMeta

	def test_8_get_DOI(self):
		"""
		The test for testing getting DOI for publishing the file.

		Skipped if the login test was failed or preparation for 
		this test case failed.
		"""
		if (not GST.logged_in):
			raise unittest.SkipTest("Skipped for failed login.")
		if (not GST.data_testing_swift_mounted):
			raise unittest.SkipTest("Skipped for failed mounting container.")
		if not GST.publishing_file_test_ready:
			raise unittest.SkipTest("Skipped for failed to prepare getting DOI test.")
		function1 = js_func["get_tags"]
		try:
			self.send_request(function1, "get_tags()")
		except Exception as e:
			raise e
		try:
			self.wait.until(EC.alert_is_present())
			alert = self.driver.switch_to_alert()
			num_before = int(unicodedata.normalize('NFKD', alert.text).encode('ascii', 'replace'))
			alert.accept()
		except Exception as e:
			raise e
		function2 = js_func["get_doi"]% (GST.gs_file_paths["file_to_publish_path"],GST.doi_info["Title"], GST.doi_info["TitleType"], GST.doi_info["Email"], GST.doi_info["Creator"],GST.doi_info["Contributors"], GST.doi_info["Description"])
		try:
			self.send_request(function2, "get_doi()")
		except Exception as e:
			raise e
		try:
			response = self.get_response()
			assert "Success" in response
		except Exception as e:
			raise Exception("Failed to get DOI of the file." + response)
		try:
			self.send_request(function1, "get_tags()")
		except Exception as e:
			raise e
		try:
			self.wait.until(EC.alert_is_present())
			alert = self.driver.switch_to_alert()
			num_after = int(unicodedata.normalize('NFKD', alert.text).encode('ascii', 'replace'))
			alert.accept()
		except Exception as e:
			raise e