'''
Module created on 21/04/2015

@author: Regina Zhang

Last Modificaiton: 23/07/2015

@description:
	the module for preparing the test cases
	checking if containers needed for the testing
	are mounted; if not, mount them
	making sure that the folders needed are present
	deleting/uploading files if needed

'''

from constants import *
from selenium.webdriver.support.ui import WebDriverWait
import time
from GStestexceptions import *
from genome_space_test import GenomeSpaceTest as GST


class DataTestPreparation(GST):

	def __init__(self, driver):
		self.driver = driver
		self.wait = WebDriverWait(driver, 60)

	def containers(self):
		'''
			method to make sure containers needed are present
		'''
		try:
			self.mounting(GST.container_names["for data tests"][0])
			self.mounting(GST.container_names["for data tests"][1])
			time.sleep(8)
			self.refresh_page()
			time.sleep(8)
		except Exception as e:
			raise PreparationException("Failed to mount the containers for data testing. " + e.__class__.__name__ + " " + e.__str__())
		try:
			self.refresh_page()
			time.sleep(8)
			assert ("swift:" + GST.container_names["for data tests"][0]) in self.driver.page_source
			assert ("swift:" + GST.container_names["for data tests"][1]) in self.driver.page_source
			GST.data_testing_swift_mounted = True
		except AssertionError:
			raise PreparationException("Containers for file tests are not connected and failed to mount them.")

	def check_dir(self, path, dir_name):
		'''
			check if one directory is present
		'''
		try:
			function1 = js_func["check_existence"] % path
			self.send_request(function1, "check_existence()")
		except Exception as e:
			raise PreparationException(("Failed to check if %s is present. ") + e.__class__.__name__ + " " + e.__str__())
		response = self.get_response()
		if "404" in response:
			function2 = js_func["create_subdir"] % path
			try:
				self.send_request(function2, "create_subdir()")
				response = self.get_response()
				assert "Success" in response
			except AssertionError:
				raise PreparationException(("Failed to create %s; response is not successful." + response) % dir_name)
		elif "Success" not in response:
			raise PreparationException(("Failed to check the existence of %s; failed with status code not 404." % dir_name) + response)
		try:
			self.send_request(function1, "check_existence()")
			response = self.get_response()
			assert "Success" in response
		except AssertionError:
			raise PreparationException(("Failed to create %s." % dir_name) + response)

	def subdirs(self):
		'''
			method to check if all directories needed are present
		'''
		self.check_dir(GST.gs_folder_paths["dir1_path"], "dir1")
		GST.dir1_exists = True
		self.check_dir(GST.gs_folder_paths["dir2_path"], "dir2")
		GST.dir2_exists = True
		if GST.default_folder_to_be_used:
			self.check_dir(default_folder_paths["dir1_path"], "default dir1")
			self.check_dir(default_folder_paths["dir2_path"], "default dir2")
			GST.default_folders_exists = True

	def remove_test_file(self, filename, file_path, testname):
		'''
			method to remove a file from GenomeSpace
		'''
		function_d = js_func["delete"] % file_path
		try:
			self.send_request(function_d, "delete_data()")
			response = self.get_response()
			assert (("Success" in response) or ("404" in response))
		except Exception as e:
			raise PreparationException(("Failed to delete the existing %s. " % filename) + response)
		try:
			function_c = js_func["check_existence"] % file_path
			self.send_request(function_c, "check_existence()")
			response = self.get_response()
			assert "404" in response
		except Exception as e:
			raise PreparationException(("Failed to prepare for the %s test." % testname) + response)

	def upload_test_file(self, filename, local_path, gs_path, testname):
		'''
			method to upload a file to GenomeSpaceTest
		'''
		try:
			f = open(local_path, "r")
			data = f.read()
		except Exception as e:
			raise PreparationException(("Failed to prepare for the %s test. " + e.__class__.__name__ + " " + e.__str__() ) % testname)
		try:
			self.uploading(filename, gs_path, data)
		except Exception as e:
			if not ("Overriding an existing object" in e.__str__()):
				raise PreparationException(("Failed to prepare for the %s test." + e.__str__() ) % testname)

	def get_file_name(self, path):
		'''
			get the file name form a given path
		'''
		tokens = path.split("/")
		name = tokens[-1]
		return name

	def files(self):
		'''
			method to make sure that the unwanted files are deleted
			(e.g. file to test uploading functionality)
			and the files needed are re-uploaded
			(e.g. file to test deleting functionality)
		'''
		failures = []
		try:
			file_name = self.get_file_name(GST.gs_file_paths["file_to_upload_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_upload_path"], "uploading")
			GST.upload_file_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			file_name = self.get_file_name(GST.gs_file_paths["after_rename_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["after_rename_path"], "changing file name")
			file_name = self.get_file_name(GST.gs_file_paths["file_to_rename_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_rename_path"], "changing file name")
			self.upload_test_file(file_name, GST.local_file_paths["file_to_rename_path"], GST.gs_file_paths["file_to_rename_path"], "changing file name")
			GST.rename_file_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			file_name = self.get_file_name(GST.gs_file_paths["file_to_generate_public_URL_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_generate_public_URL_path"], "generating public URL")
			self.upload_test_file(file_name, GST.local_file_paths["file_to_generate_public_URL_path"], GST.gs_file_paths["file_to_generate_public_URL_path"], "generating public URL")
			GST.generate_public_URL_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			file_name = self.get_file_name(GST.gs_file_paths["file_to_copy_source_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_copy_source_path"], "copying data")
			self.upload_test_file(file_name, GST.local_file_paths["file_to_copy_source_path"], GST.gs_file_paths["file_to_copy_source_path"], "copying data")
			file_name = self.get_file_name(GST.gs_file_paths["copy_to_folder_target_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["copy_to_folder_target_path"], "copying data")
			file_name = self.get_file_name(GST.gs_file_paths["copy_to_container_target_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["copy_to_container_target_path"], "copying data")
			GST.copying_data_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			file_name = self.get_file_name(GST.gs_file_paths["file_to_move_to_folder_source_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_move_to_folder_source_path"], "moving data")
			self.upload_test_file(file_name, GST.local_file_paths["file_to_move_to_folder_source_path"], GST.gs_file_paths["file_to_move_to_folder_source_path"], "moving data")
			file_name = self.get_file_name(GST.gs_file_paths["file_to_move_to_container_source_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_move_to_container_source_path"], "moving data")
			self.upload_test_file(file_name, GST.local_file_paths["file_to_move_to_container_source_path"], GST.gs_file_paths["file_to_move_to_container_source_path"], "moving data")
			file_name = self.get_file_name(GST.gs_file_paths["move_to_folder_target_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["move_to_folder_target_path"], "moving data")
			file_name = self.get_file_name(GST.gs_file_paths["move_to_container_target_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["move_to_container_target_path"], "moving data")
			GST.moving_data_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			file_name = self.get_file_name(GST.gs_file_paths["file_to_delete_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_delete_path"], "deleting data")
			self.upload_test_file(file_name, GST.local_file_paths["file_to_delete_path"], GST.gs_file_paths["file_to_delete_path"], "deleting data")
			GST.deleting_data_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			file_name = self.get_file_name(GST.gs_file_paths["file_to_publish_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_publish_path"], "getting DOI")
			self.upload_test_file(file_name, GST.local_file_paths["file_to_publish_path"], GST.gs_file_paths["file_to_publish_path"], "getting DOI")
			GST.publishing_file_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			file_name = self.get_file_name(GST.gs_file_paths["file_to_import_to_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_import_to_path"], "importing file using public url")
			file_name = self.get_file_name(GST.gs_file_paths["file_to_import_with_URL_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_import_with_URL_path"], "importing file using public url")
			self.upload_test_file(file_name, GST.local_file_paths["file_to_import_with_URL_path"], GST.gs_file_paths["file_to_import_with_URL_path"], "importing file using public url")
			GST.importing_url_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			file_name = self.get_file_name(GST.gs_file_paths["file_to_launch_GVL_with"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_launch_GVL_with"], "launching Galaxy with file")
			self.upload_test_file(file_name, GST.local_file_paths["file_to_launch_GVL_with"], GST.gs_file_paths["file_to_launch_GVL_with"], "launching Galaxy with file")
			GST.launch_GVL_with_file_test_ready = True
		except Exception as e:
			failures.append(e)
		if failures != []:
			report = ""
			for item in failures:
				report = report + item.__class__.__name__ + ": " + item.__str__() + "\n"
			raise PreparationException(report)

	def test_3_setting_up(self):
		'''
			method to prepare for the following test cases
			making sure that containers, folders and files are all ready
		'''
		self.containers()
		exception = None
		try:
			self.subdirs()
		except Exception as e:
			exception = e
		self.files()
		if exception:
			raise exception


