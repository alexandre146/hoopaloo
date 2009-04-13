# coding: utf-8

#Hoopaloo - Version 1.0 - 2008/2009
#Author: Mariana Romao do Nascimento - mariana@dsc.ufcg.edu.br

import subprocess, os, signal
from datetime import datetime
from django.conf import settings
from django.core import *
from hoopaloo.models import Submission, Execution
import configuration 
import queries
import util

class Tester:
	'''This class realize teh execution of a test to the students' program.
	It uses the module subprocess that creates a new process in order to execute the test.'''
	
	def __init__(self, s, t, id_exercise, submission=None):
		'''The constructor. It receive the student, the test and the exercise involved in execution'''
		self.student = s
		self.test = t
		self.exercise = id_exercise
		self.infinite_loop = False
		self.process = None
		self.cron_finish = False
		if submission:
			self.submission = submission
		
	def get_message_to_student(self, log):
		'''Makes the message of error to the student.
		If the teacher registered a message in the tests shows this message. If not, shows the message defaulst of assertion error'''
		msg = ""
		for l in log:
			line = str(l)
			if line.startswith("AssertionError"):
				s = line.split(":")
				try:
					msg = s[1] + '\n'
				except:
					pass
		return msg
		
	
	def execute_test(self):
		'''Realize the execution of test.'''
		
		test_file_name = self.test.path
		student_username = self.student.username
		# Verifies if the student realize some submission to this exercise
		num_submissions = queries.get_number_student_submissions(self.exercise, self.student.id)
		if num_submissions > 0:
			# the path of test in students' folder
		
			test_file_path = settings.MEDIA_ROOT + '/' + student_username + '/' + self.exercise.name + '/' + test_file_name
			
			#from threading import Timer
			#cron = Timer(17.0, self.infinite_loop_func)
			#cron.start()
			
			# command to execute the test
	
			cmd = ['python', test_file_path]
			self.process = subprocess.Popen(args=cmd)
			self.process.wait()
			# against infinite loop
			
			self.register_results()
			
			sub = queries.get_last_submission(self.exercise, self.student.id)
			sub.was_executed = True
			sub.save()
		
	def execute_under_test(self):
		 test_file_name = self.test.path
		 test_file_path = settings.MEDIA_ROOT + '/under_tests/' + test_file_name
		 #copying temporarly the student file to folder 'under_tests'
		 
		 original_file_path = self.submission.solution_file.name
		 copy_file_path = settings.MEDIA_ROOT + '/under_tests/' + self.exercise.name + '.py'
		 util.copy_file(original_file_path, copy_file_path)
		 
		 cmd = ['python', test_file_path]
		 self.process = subprocess.Popen(args=cmd)
		 self.process.wait()
		 
		 #Removing the student file of folder 'under_tests'
		 os.remove(copy_file_path)
		 
		 return self.register_temp_results()
		 
	def register_temp_results(self):
		
		num_errors = 0
		num_failures = 0
		num_tests = 0
		was_success = False
		msg_to_student = ''
		loop = False
		try:
			result_file = open(settings.MEDIA_ROOT + '/under_tests/' + configuration.RESULT_TEST_FILE)
			results = result_file.readlines()
			
			num_errors = int(results[0])
			num_failures = int(results[1])
			num_tests = int(results[2])
			was_success = bool(results[3])
			log_errors = results[4:]
			
			msg_to_student = self.get_message_to_student(log_errors)
			result_file.close()
			os.remove(settings.MEDIA_ROOT + '/under_tests/' + configuration.RESULT_TEST_FILE)
		
		except:
			try:
				# some error of syntax or import occourred
				result_file = open(settings.MEDIA_ROOT + '/errors/result.txt')
				results = result_file.readlines()
				for r in results:
					msg_to_student += str(r)
				result_file.close()
				os.remove(settings.MEDIA_ROOT + '/errors/result.txt')
				log_errors = msg_to_student
				
				if log_errors == configuration.INFINITE_LOOP_MSG:
					loop = True
			except:
				return
			
		return util.Temp_Results(self.student, self.submission, num_errors, num_failures, num_tests, log_errors)
			 
	def infinite_loop_func(self):
		"""Function to terminate a execution when it will be infinite loop"""
		
		if not os.path.exists(settings.MEDIA_ROOT + '/' + self.student.username + '/' + self.exercise.name + '/' + configuration.RESULT_TEST_FILE):
			self.infinite_loop = True
			file_error = open(settings.MEDIA_ROOT + "/errors/result.txt", 'wb')
			file_error.write(configuration.INFINITE_LOOP_MSG)
			file_error.close()
		
			id_process = self.process.pid
			os.kill(id_process, signal.SIG_IGN)
		
		self.cron_finish = True
		
	def register_results(self):
		'''This method register the result of execution in a temporary file.
		The results are based in TestResult object (see module unittest)'''
		num_errors = 0
		num_failures = 0
		num_tests = 0
		was_success = False
		msg_to_student = ''
		loop = False
		try:
			result_file = open(settings.MEDIA_ROOT + '/' + self.student.username + '/' + self.exercise.name + '/' + configuration.RESULT_TEST_FILE)
			results = result_file.readlines()
		
			num_errors = int(results[0])
			num_failures = int(results[1])
			num_tests = int(results[2])
			was_success = bool(results[3])
			log_errors = results[4:]
		
			msg_to_student = self.get_message_to_student(log_errors)
			result_file.close()
			os.remove(settings.MEDIA_ROOT + '/' + self.student.username + '/' + self.exercise.name + '/' + configuration.RESULT_TEST_FILE)
		
		except:
			try:
				# some error of syntax or import occourred
				result_file = open(settings.MEDIA_ROOT + '/errors/result.txt')
				results = result_file.readlines()
				for r in results:
					msg_to_student += str(r)
				result_file.close()
				os.remove(settings.MEDIA_ROOT + '/errors/result.txt')
				log_errors = msg_to_student
				
				if log_errors == configuration.INFINITE_LOOP_MSG:
					loop = True
			except:
				return
				
		if num_tests != 0:
			self.exercise.number_tests = num_tests
			if (num_errors == 0) and (not self.infinite_loop):
				self.exercise.number_students_that_solved = queries.number_students_that_solved(self.exercise.id) + 1
			self.exercise.save()
			
		# Storing the execution of a test
		execution = Execution()
		
		sb = queries.get_last_submission(self.exercise.id, self.student.id)
		
		execution.id_submission = sb
		execution.id_student = self.student
		execution.id_test = self.test
		execution.errors_number = num_errors + num_failures
		execution.pass_number = num_tests - (num_errors + num_failures)
		execution.date = datetime.now()
		execution.errors_to_student = msg_to_student
		execution.was_success = was_success
		execution.loop = loop
		
		for e in log_errors:
			execution.log_errors += e
			
		execution.save()
		