'''
Module Created on 08/12/2014

@author: Regina Zhang

Last Modification: 23/07/2015

@description:
    module for testing data sharing functionality
        generating public URL of a file

'''

import unittest
from abc import ABCMeta
from GStestexceptions import *
from constants import *
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from _codecs import register
from selenium.webdriver.common.action_chains import ActionChains
import unicodedata

from genome_space_test import GenomeSpaceTest as GST


class DataSharing(GST):
    
    __metaclass__ = ABCMeta
    
    def test_5a_generate_public_URL(self):
        """
        The test for testing generating public URL of the file in GenomeSpace.
        
        Skipped if the login test was failed or preparation for 
        this test case failed.
        """
        if (not GST.logged_in) or (not GST.data_testing_swift_mounted):
            raise unittest.SkipTest("Skipped for failed login or failed mounting container.")
        elif not GST.generate_public_URL_test_ready:
            raise unittest.SkipTest("Skipped for failed to prepare generating public URL test.")
        self.dismiss_dialogs()
        function = js_func["generate_public_url"] % GST.gs_file_paths["file_to_generate_public_URL_path"]
        try:
            self.send_request(function, "generate_public_url()")
        except Exception as e:
            raise PublicURLException("Failed to generate public URL.\n" + e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            time.sleep(2)
        except AssertionError:
            self.get_response()
            raise PublicURLException("Failed to generate public URL.\n" + response)
        try:
            self.wait.until(EC.alert_is_present())
            alert = self.driver.switch_to_alert()
            assert "Public URL" in alert.text
        except TimeoutException:
            raise PublicURLException("Failed to catch public URL pop-up.")
        except AssertionError:
            raise PublicURLException("Failed to get generated public URL.")
        try:
            public_url = alert.text.lstrip("Public URL: ")
            alert.accept()
            public_url = unicodedata.normalize('NFKD', public_url).encode('ascii', 'replace')
            function = js_func["download_file"] % (public_url)
            self.send_request(function, "download_file()")
        except Exception as e:
            raise PublicURLException("Failed to share data using public URL generated.\n" + e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise PublicURLException("Failed to share data using public URL generated.\n" + response)
