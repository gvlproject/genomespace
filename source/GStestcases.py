'''
Module created on 26/11/2014

@author: Regina Zhang

Last Modification: 23/07/2015

@description:
	a module for bringing all the test cases together

'''

import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from constants import *
import time
from abc import ABCMeta, abstractmethod
from registration_login import RegistrationLogin
from mount_disconnect import CloudStorage
from data_manipulation import DataManipulation
from data_sharing import DataSharing
from data_storing import DataStoring
from data_to_GVL import DataToGVL
from data_test_preparation import DataTestPreparation
from file_publish import FilePublish



class GSTestCases(RegistrationLogin, CloudStorage, DataTestPreparation, DataManipulation, DataSharing, DataStoring, DataToGVL, FilePublish):

    __metaclass__ = ABCMeta

    

