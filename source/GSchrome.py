'''
Module created on 26/11/2014

@author: Regina Zhang

'''

import unittest
from GStestcases import GSTestCases
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from constants import *
import pickle
import chrome_path
from genome_space_test import GenomeSpaceTest as GST
import sys


class GSChrome(unittest.TestCase, GSTestCases):

    @classmethod
    def setUpClass(cls):
        '''
            a class method overriding Unittest setUpClass method
            preparation work before the testing starts
        '''
        cls.parse_config()
        cls.driver_name = "chrome"
        chrome_driver_path = chrome_path.driver_path
        if chrome_driver_path != None:
            cls.driver = webdriver.Chrome(executable_path = chrome_driver_path)
        else:
            cls.driver = webdriver.Chrome()
        driver = cls.driver
        driver.implicitly_wait(10)
        cls.wait = WebDriverWait(driver,60)
        driver.maximize_window()
        home_page = common["base_url"] + common["home_suffix"]
        try:
            driver.get(home_page)
            driver.implicitly_wait(20)
            assert "No results found." not in driver.page_source
        except UnexpectedAlertPresentException:
            alert = driver.switch_to_alert()
            text = alert.text
            alert.accept()
            print >>sys.stderr, ("Unexpected alert present: " + text)
        except AssertionError:
            driver.close()
            raise Exception("Page not found: " + home_page)
        if GST.developing:
            # load the cookie stored last time.
            # if cookie expired, manual deletion needed
            try:
                cookie_file_name = "cookies_" + cls.driver_name + ".pkl"
                cookies = pickle.load(open(cookie_file_name,"rb"))
                for cookie in cookies:
                    driver.add_cookie(cookie)
                GST.logged_in = True
            except IOError:
                GST.logged_in = False
        try:
            driver.get(home_page)
            driver.implicitly_wait(20)
            assert "No results found." not in driver.page_source
        except AssertionError:
            driver.close()
            raise Exception("Page not found: " + home_page)
        except UnexpectedAlertPresentException:
            alert = driver.switch_to_alert()
            text = alert.text
            alert.accept()
            print >>sys.stderr, ("Unexpected alert present: " + text)

    @classmethod
    def tearDownClass(cls):
        '''
            a class method overriding the tearDownClass method in Unittest
            close browser and quit driver when the test is done
        '''
        cls.driver.close()
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)
