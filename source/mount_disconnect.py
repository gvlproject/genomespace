'''
Module created on 08/12/2014

@author: Regina Zhang

Last Modification: 23/07/2015

@description:
    module for testing mounting container to GenomeSpace
    and disconnecting container 

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
from genome_space_test import GenomeSpaceTest as GST
from data_test_preparation import DataTestPreparation

passed_mounting = False

class CloudStorage(GST):
    
    __metaclass__ = ABCMeta


    def test_2a_mount_container(self):
        """
        The test for mounting container functionality of GenomeSpace.
        
        Skipped if the login test was failed.
        """
        if not GST.logged_in:
            raise unittest.SkipTest("Skipped for failed login.")
        driver = self.driver
        wait = self.wait
        try:
            self.mounting(GST.container_names["for mounting test"])
            global passed_mounting
            passed_mounting = True
        except Exception as e:
            raise e
        

    def test_2b_disconnect_container(self):
        """
        The test for testing the disconnect container functionality of GenomeSpace.
        
        Skipped if the login test or mounting container test was failed.
        """
        global passed_mounting
        if (not GST.logged_in) or (not passed_mounting):
            raise unittest.SkipTest("Skipped for failed login or mounting.")
        function = js_func["disconnect"]  % (GST.user_details["username"], GST.container_names["for mounting test"])
        try:
            self.send_request(function, "disconnect()")
        except Exception as e:
            raise DisconnectContainerException(e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise DisconnectContainerException(response)
