'''
Module created on 08/12/2014

@author: Regina Zhang

Last Modification: 23/07/2015

@description:
    module for testing if a (potential) user can get access
    to GenomeSpace
        register to GenomeSpace
        login to GenomeSpace

'''

import pickle
import unittest
from abc import ABCMeta
from GStestexceptions import *
from constants import *
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from genome_space_test import GenomeSpaceTest as GST
import sys

class RegistrationLogin(GST):
    
    __metaclass__ = ABCMeta

    def test_1a_register(self):
        """
        The test for testing the registration of GenomeSpace.
        
        The registration is expected to fail as the account 
        used for testing already exists.
        """
        if GST.logged_in == True:
            raise unittest.SkipTest("Logged in")
        driver = self.driver
        wait = self.wait
        try:
            link = page_register['link_text']
            elem = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, link)))
            elem = driver.find_element_by_link_text(link)
            elem.click()
            elem = driver.find_element_by_id(page_register["username"])
            elem.send_keys(GST.user_details["username"])
            elem = driver.find_element_by_id(page_register["pw"])
            elem.send_keys(GST.user_details["password"])
            elem = driver.find_element_by_id(page_register["email"])
            elem.send_keys(GST.user_details["email"])
            elem = driver.find_element_by_id(page_register["signup_button"])
            elem.click()
            time.sleep(5)
            assert "Cannot create duplicate username" in driver.page_source
            driver.get(common["base_url"]+common["home_suffix"])
        except UnexpectedAlertPresentException:
            alert = driver.switch_to_alert()
            text = alert.text
            alert.dismiss()
            print >>sys.stderr, ("Unexpected alert present: " + text)
            driver.get(common["base_url"]+common["home_suffix"])
        except NoSuchElementException as e:
            messages = e.__str__().split("\n")
            self.dismiss_dialogs()
            raise RegistrationException(messages[0])
        except AssertionError:
            raise RegistrationException("Failed to assert the error message.")
        finally:
            driver.get(common["base_url"]+common["home_suffix"])

    def test_1b_login(self):
        """
        Test for testing the login functionality of GenomeSpace.
        
        This test is the prerequisite for every other tests of GenomeSpace,
        as all the rest tests are done in the account used for this test.
        """
        if GST.logged_in == True:
            raise unittest.SkipTest("Logged in")
        driver = self.driver
        wait = self.wait
        try:
            # try if an alert popped up
            alert = driver.switch_to_alert()
            print "Alert popped up and dismissed: " + alert.text
            alert.dismiss()
        except NoAlertPresentException:
            pass
        try:
            # wait until the page is loaded and ready
            elem = wait.until(EC.element_to_be_clickable((By.ID, page_login['login_name'])))
        except TimeoutException:
            driver.close()
            raise LoginException("Timed out loading page before login.")
        try:
            elem = driver.find_element_by_id(page_login['login_name'])
            elem.clear()
            elem.send_keys(GST.user_details['username'])
            elem = driver.find_element_by_id(page_login['login_pw'])
            elem.clear()
            elem.send_keys(GST.user_details['password'])
            elem = driver.find_element_by_id(page_login['login_signin'])
            elem.click()
            driver.implicitly_wait(10)
            assert "Invalid username or password" not in driver.page_source
            elem = wait.until(EC.element_to_be_clickable((By.ID, common["menu_file"])))
            time.sleep(20)
        except AssertionError as e:
            driver.close()
            raise LoginException("Invalid username or password", GST.user_details['username'], GST.user_details['password'])
        except TimeoutException:
            # failed to load the page after logging in
            driver.close()
            raise LoginException("Timed out loading page when logging in.", GST.user_details['username'], GST.user_details['password'])
        except NoSuchElementException as e:
            messages = e.__str__().split("\n")
            driver.close()
            raise LoginException(messages[0])
        except UnexpectedAlertPresentException:
            alert = driver.switch_to_alert()
            text = alert.text
            alert.dismiss()
            raise LoginException("Unexpected alert present: " + text)
        except Exception as e:
            driver.close()
            raise LoginException("Failed logging in: "+e.__str__(), GST.user_details['username'], GST.user_details['password'])
        if GST.developing:
            # store the cookie for quick debuging when the program is under development
            cookie_file_name = "cookies_" + self.driver_name + ".pkl"
            pickle.dump(driver.get_cookies(), open(cookie_file_name, "wb"))
        GST.logged_in = True
