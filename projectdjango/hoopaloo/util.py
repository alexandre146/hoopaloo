# coding: utf-8

#Hoopaloo - Version 1.0 - 2008/2009
#Author: Mariana Romao do Nascimento - mariana@dsc.ufcg.edu.br

import smtplib
import random
import sha
import os
import re
from unicodedata import normalize
from datetime import date, datetime, timedelta
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
import configuration
import queries


def generate_aleatory_password():
	"""Generates a new password randomly"""
	
	import string
	from random import choice
	size = 6 # the length of password
	return ''.join([choice(string.letters + string.digits) for i in range(size)])
	
def send_email(email_to, subject, message):
	"""Sends a new email message using the lib smtplib"""
	
	msg = {}
	msg['From']=configuration.EMAIL_SYSTEM # the system email
	msg['To']=email_to
	msg['Subject'] = "[Hoopaloo] " + subject
	msg['Message'] = message

	servidor = smtplib.SMTP() # the address of smtp server
	smtpserver = configuration.SMTP_SERVER
	servidor.connect(smtpserver,25)
	text = "From: %s\nTo: %s\nSubject: %s\n%s" % (msg['From'], msg['To'], msg['Subject'], msg['Message'])
	servidor.sendmail(msg['From'], msg['To'], text)
	servidor.quit()

	
def send_new_password(self, email, user):
	"""Send to the user a new password generated automatically"""
	
	pwd = generate_aleatory_password()
	user.set_password(pwd)
	new_password = user.password
	user.save()
	profile = user.get_profile()
	profile.realized_login = False
	profile.save()
	
	msg = configuration.FORGOT_PASSWORD_EMAIL % (smart_str(user.first_name), smart_str(pwd))
	subject = "Your New Password"
	send_email(email, subject, msg)
		
def listToString(list):
	"""Converts the elements of a list in string"""
	
	r = []
	for element in list:
		r = element + '\n'
	return r
	

def isValidUsername(field_data):
	"""Verifies if the username provided is valid.
	An username is valid when there are not an equal username in database."""
	
	try:
		queries.get_user_from_username(field_data)
		return False
	except User.DoesNotExist:
		return True
	
def isValidEmail(email):
	"""Verifies if the email is valid.
	An email is valid when follows the form: something@something.something."""
	
	try:
		div = email.split('@')
		part = div[1].split('.')
		if len(part) >= 2:
			return True
		else:
			return False
	except:
		return False
		
def isValidStudentID(studentID):
	"""Verifies is the studentID of a student is valid.
	An studentID is valid when the number has 8 (eight) digits."""
	
	try:
		int(studentID)
		exp = re.compile('\d{8}$')
		result = exp.match(str(studentID))
		if not result:
			return False
		return True
	except:
		return False
		
def make_message_student(result):
	"""Makes a message to student.
	If the result is PASS the message shows the number of tests.
	If the result is FAIL the message shows the number of tests, the number of errors and right and the messages of errors"""
	from hoopaloo.models import Execution, Submission

	msgs = []

	if result == None:
		msg = configuration.EXECUTION_AFTER
		msgs.append(msg)
		return None, msgs
	else:
		submission = queries.get_last_submission(result.id_exercise.id, result.id_student.id)
		execution = queries.get_last_execution(submission.id)
		if result.veredict == "Pass":
			msg = configuration.EXECUTION_PASS % (result.pass_number)
			msgs.append(msg)
			return True, msgs
		elif (result.veredict == "Fail") and (execution.loop):
			msg = configuration.EXECUTION_LOOP 
			msgs.append(msg)
			return False, msgs
			
		elif result.veredict == "Fail":
			msg = configuration.EXECUTION_FAILED % (result.pass_number + result.errors_number, result.errors_number)
			msgs.append(msg)
			lines = result.errors_to_student.split('\n')
			for l in lines:
				if l != "":
					msgs.append(l)
			return False, msgs
			
def notify_students(students, id_ex):
	"""Notify the students about the result of execution tests."""
	
	from hoopaloo.models import Submission
	for s in students:
		submissions = queries.get_number_student_submissions(id_ex, s.id)
		if submissions.count() != 0:
			last_submission = queries.get_last_submission(id_ex, s.id)
			if last_submission.date <= test_creation_date:
				veredict, message = make_message_student(last_submission)
				
				subject = "Notification"
				send_email(s.user.email, subject, message)
				
def register_action(user, action):
	"""Register the action executed by user in database"""
	
	from hoopaloo.models import Actions_log
	log = Actions_log().create_action(user, action, datetime.now())
	log.save()
	
def update_students(exercise):
	"""Updates some informations of student like number of solved exercises and number of unsolved exercises.
	This method is invoked when an exercise change your availability."""

	students = queries.get_all_students()
	for s in students:
		try:
			submission = queries.get_last_submission(exercise.id, s.id)
			if submission.veredict == 'Pass':
				s.solved_exercises = queries.get_number_solved_exercises(s.id) + 1
			else:
				s.unsolved_exercises = queries.get_number_unsolved_exercises(s.id) + 1
		except:
			s.undelivered_exercises = queries.get_number_undelivered_exercises(s.id) + 1
		s.pending_exercises = queries.get_number_available_exercises() - 1
		s.save()
	
class DateException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
		
def get_time_unavailability(date_f, date_i):
	"""Returns the number of seconds that a exercise will be available (duration of availability of an exercise)"""
	
	date_result = date_f - date_i
	if date_result.days < 0:
		raise DateException, 'The date is invalid'
	time = date_result.days*24*60*60 + date_result.seconds + (date_result.microseconds/1000000.0)
	return time

def get_next_friday(today):
	"""Returns the next friday from a today."""
	
	import calendar
		
	calendar.setfirstweekday(calendar.SUNDAY)

	if (calendar.weekday(today.year, today.month, today.day) == 0):
		delta = timedelta(4)
	elif (calendar.weekday(today.year, today.month, today.day) == 1):
		delta = timedelta(3)
	elif (calendar.weekday(today.year, today.month, today.day) == 2):
		delta = timedelta(2)
	elif (calendar.weekday(today.year, today.month, today.day) == 3):
		delta = timedelta(1)
	elif (calendar.weekday(today.year, today.month, today.day) == 4):
		delta = timedelta(0)
	elif (calendar.weekday(today.year, today.month, today.day) == 5):
		delta = timedelta(6)
	else:
		delta = timedelta(5)
	
	return today + delta
	
def first_access(user):
	"""Returns True if the first access of the user and False if not"""
	
	try:
		profile = user.get_profile()
		if not profile.realized_login:
			return True
		else:
			return False
	except:
		pass
		
		
class Change_Availability():
	"""Class to express the availability of an exercise. It is who start the thread that count the time of availabilty of an exercise."""
	
	def __init__(self, exercise_name, t):
		self.exercise_name = exercise_name
		self.time = t
		
	def change_availability(self):
		"""Change the availability of an exerciese."""
		from hoopaloo.models import Exercise
		exercise = queries.get_exercise_from_name(self.exercise_name)
		exercise.available = False
		exercise.save()
	
	def init_cont(self):
		"""Starts the thread of time"""
		from threading import Timer
		cron = Timer(self.time, self.change_availability)
		cron.start()
	
class MyTuple:
	"""Class to facilitate the manipulation of tuples in HTML file using the language of templates of Django."""
	
	def __init__(self, x, y, z=None):
		self.x = x
		self.y = y
		self.z = z
	
def calculate_percentual(percentual_list, number_tests, students, exercise):
	"""Returns a list in which each element has a percentual.
	This percentual is a percent of test right. For example: 20% of class passed in 40% of tests."""
	
	result_p = []
	for p in percentual_list:
		num = 0
		for s in students:
			try:
				last_submission = queries.get_last_submission(exercise.id, s.id)
				execution = queries.get_last_execution(last_submission.id)
				aux = (execution.pass_number * 100) / exercise.number_tests
				if aux <= p[0] or aux >= p[1]:
					num += 1
			except:
				pass
		element = MyTuple("%s - %s" % (p[1], p[0]), num*100/len(students) )
		result_p.append(element)
	return result_p

def calculate_score_percentual(percentual_list, results, exercise):
	"""Returns a list in which each element has a percentual.
	This percentual is a percent of note. For example: 20% of class received note between 8 and 9."""
	
	result_p = []
	count = 0
	for p in percentual_list:
		num = 0
		for r in results:
			if r.score <= p[0] and r.score >= p[1]:
				num += 1
		if len(results) > 0:
			element = MyTuple("%.1f - %.1f" % (p[0], p[1]), num*100/len(results), count)
		else:
			element = MyTuple("%.1f - %.1f" % (p[0], p[1]), 0, count)
		result_p.append(element)
		count += 1
	return result_p
	
def mean(results):
	"""Calculates the arithmetic mean of elements of the parameter "results" """
	
	mean = 0
	sum = 0
	count = 0
	for r in results:
		if r.score != None:
			sum += r.score
			count +=1
	if len(results) != 0 and count != 0:
		mean = sum/count
	return mean
	
def calculate_mean_student(student):
	"""Calculates the mean of note of a student"""
	exercises = queries.get_unavailable_exercises()
	results = []
	for ex in exercises:
		try:
			last_submission = queries.get_last_submission(ex.id, student.id)
			results.append(last_submission)
		except:
			pass
	return mean(results)

def calculate_mean(exercise):
	"""Calculates the mean of notes of an exercise"""
	
	students = queries.get_all_students()
	results = []
	for st in students:
		try:
			last_submission = queries.get_last_submission(exercise.id, st.id)
			results.append(last_submission)
		except:
			pass
	return mean(results)
			
def get_students_percent(index, id_ex):
	"""Returns the students that passed in specific percentual tests"""
	
	students = queries.get_all_students()
	exercise = queries.get_exercise(id_ex)
	st_percent = []
	
	percent = configuration.PERCENT_OF_TESTS[index]
	percent1 = percent[0]
	percent2 = percent[1]
	
	for s in students:
		aux = 0
		try:
			last_submission = queries.get_last_submission(id_ex, s.id)
			execution = queries.get_last_execution(last_submission.id)
			aux = (execution.pass_number * 100) / exercise.number_tests
			if (aux >= float(percent1) and aux <= float(percent2)):
				st_percent.append(s)
		except:
			pass

	return st_percent

def get_students_score_percent(index, id_exercise):
	"""Returns the students that has a specific score (referenced by index)"""
	
	from hoopaloo.models import Exercise, Student, Result
	students = queries.get_all_students()
	exercise = queries.get_exercise(id_exercise)
	st_percent = []

	score = configuration.PERCENT_OF_SCORE[index]
	score1 = score[1]
	score2 = score[0]

	for s in students:
		aux = 0
		try:
			last_submission = queries.get_last_submission(exercise.id, s.id)
			if (last_submission.score >= float(score1) and last_submission.score <= float(score2)):
				st_percent.append(s)
		except:
			pass
	return st_percent
	
def calculate_correct_percentage(exercise):
	"""Calculate the percentage of right tests of all students to an specific exercise"""
	
	students = queries.get_all_students()
	percent = 0 
	for s in students:
		try:
			last_submission = queries.get_last_submission(exercise.id, s.id)
			if last_submission.veredict == 'Pass':
				percent +=1 
		except:
			pass
	return (percent*100)/students.count()
	
def is_assistant(user):
	if user.is_superuser:
		return False
	return True
	
def get_available_exercises(user):
	available = queries.get_available_exercises()
	student = user.get_profile()
	undelivered = []
	for ex in available:
		submited = queries.get_number_student_submissions(ex.id, student.id)
		if submited == 0:
			undelivered.append(ex)
	return undelivered	
	
def add_score_and_comments(comments, score, exercise, submission):
	
	has_error = False
	error = ''
	if comments != "":
		submission.comments = comments
	if score != "":
		try:
			n = int(score)
		except:
			try:
				n = float(score)
			except:
				error = configuration.ADD_NOTE_ERROR
				has_error = True
	
		if n > 10 or n < 0:
			error = configuration.ADD_NOTE_ERROR_2
			has_error = True
		else:
			submission.score = n
	submission.save()
	exercise.mean_notes = calculate_mean(exercise)
	exercise.save()
	student = queries.get_student(submission.id_student.id)
	student.mean = calculate_mean_student(student)
	student.save()
	return has_error, error
	
def update_availability(id_exercise):
	
	ex = queries.get_exercise(id_exercise)
	if ex.available == True:
		available = False
		update_students(ex)
		ex.number_students_that_solved = queries.number_students_that_solved(ex)
	else:
		available = True
		ex.date_availability = datetime.today()
		students = queries.get_all_students()
		for s in students:
			s.pending_exercises = s.pending_exercises + 1
			s.save()
		#init the cron
		try:
			t = get_time_unavailability(ex.date_finish, ex.date_availability)
		except:
			return False
		cron = Change_Availability(ex.name, t)
		cron.init_cont()
	
	ex.available = available
	ex.save()
	return True

def get_delivered_exercises(student_id):
	from hoopaloo.models import Exercise
	available = queries.get_reverse_ordered_available_exercises()
	delivered = []
	for ex in available:
		try:
			submited = queries.get_last_submission(ex.id, student_id)
			execution = queries.get_last_execution(submited.id)
			if submited.veredict == 'Pass':
				solved = True
			else:
				solved = False
			percentage = calculate_correct_percentage(ex)
			d = Table_Delivered(ex, result.num_submissions, submited.date, ex.number_tests, solved, execution.errors_number, submited.score, percentage)
			delivered.append(d)
		except:
			pass
	return delivered
		
def copy_test_files(student):
	"""Copy all test files in the student folder"""
	
	exercises = queries.get_all_exercises()
	for e in exercises:
		path_student = settings.MEDIA_ROOT + '/' + student.username + '/' 
		try:
			test = queries.get_consolidate_test(e.id)
			student_test = open(path_student + test.path, 'wb')
			file_test = open(settings.MEDIA_ROOT + '/tests/' + test.path, 'rb')
			lines = file_test.readlines()
			contend = ''
			for l in lines:
				contend += l
				
			if contend.__contains__("from pexpect import *"):
				number = contend.count('%')
				aux = number*(path_student,)
				student_test.write((contend % aux ) + configuration.TEST_APPEND_STUDENT_FOLDER % (test.name, path_student))
			else:
				student_test.write(contend  + configuration.TEST_APPEND_STUDENT_FOLDER % (test.name, path_student))
			
			student_test.close()
			file_test.close()
			
		except:
			# have not test for this exercise
			pass

		
def change_test(original_test, changed_test):
	
	exercise = queries.get_exercise(original_test.exercise.id)
	
	# exists a copy of test file is in '/tests/'
	old_file_path = settings.MEDIA_ROOT + '/tests/' + original_test.path
	# the name of back up file following the form: /tests/backup_test_<exercise_name>.py
	backup_file = open(settings.MEDIA_ROOT + '/tests/' + configuration.BACKUP_TEST_NAME + '_' + exercise.name + '.py', 'wb')
	# open the old file of tests in order to read it
	file = open(old_file_path, 'rb')
	
	# write the contend of the old file in back up file
	backup_file.write(file.read())
	backup_file.close()
	file.close()
	# remove the old file of tests
	os.remove(old_file_path)
	
	path_under_test = settings.MEDIA_ROOT + '/under_tests/' + changed_test.path
	os.remove(path_under_test)
	
	# save the new conted of test
	path_tests = settings.MEDIA_ROOT + '/tests/' + original_test.path
	dest = open(path_tests, 'wb')
	
	new_test_code = changed_test.code.replace('undertest_', 'test_')
	new_test_code = new_test_code.replace('UnderTest_', 'Test_')
	
	dest.write(new_test_code + '\n\n\n' + configuration.TEST_APPEND)
	dest.close()
			
	students = queries.get_all_students()
	# in this loop, delete the old test files that were in students' folders
	for s in students:
		usr = s.username
		path_student = settings.MEDIA_ROOT + '/' + usr + '/' + exercise.name + '/'
		old_file_students_path = path_student + original_test.path
		os.remove(old_file_students_path)
		
		test_full_path =  path_student + original_test.path
		if not os.path.exists(path_student):
			os.makedirs(path_student)
		
		dest = open(test_full_path, 'wb')
		if new_test_code.__contains__("from pexpect import *") or new_test_code.__contains__("import pexpect"):
			number = new_test_code.count('%')
			aux2 = number*(path_student,)
			dest.write((new_test_code % aux2) + '\n\n\n' + (configuration.TEST_APPEND_STUDENT_FOLDER % (original_test.name, "'" + path_student + "'")))
		else:
			dest.write(new_test_code + '\n\n\n' + configuration.TEST_APPEND_STUDENT_FOLDER % (original_test, "'" + path_student + "'"))
		dest.close()
		
	original_test.code = new_test_code
	original_test.locked = False
	original_test.locked_by = "Anyone"
	
	changed_test.delete()
	original_test.save()
	
def save_under_test_file(test):
	exercise = queries.get_exercise(test.exercise.id)
	# save the new conted of test
	path_tests = settings.MEDIA_ROOT + '/under_tests/' + test.path
	dest = open(path_tests, 'wb')
	
	aux = "'" + path_tests + "'"
	if test.code.__contains__("from pexpect import *"):
		number = test.code.count('%')
		aux2 = number*(path_tests,)
		dest.write((test.code % aux2) + (configuration.UNDER_TEST_COMPLEMENT % aux, aux))
	else:
		dest.write(test.code + '\n\n\n' + configuration.UNDER_TEST_COMPLEMENT % (test.name, "'" + settings.MEDIA_ROOT + '/under_tests/' + "'"))
	dest.close()
	
			
def create_datetime(d):

	pieces = d.split(" ")
	date = pieces[0]
	time = pieces[1]
	year, month, day = date.split("-")
	hour, minutes = time.split(":")
	
	return datetime(int(year), int(month), int(day), int(hour), int(minutes))
	
def remove_acentuation(code):
	return normalize('NFKD', code.decode('iso-8859-7')).encode('ASCII', 'ignore')

def copy_file(souce, destination):
	source_file = open(souce, 'rb')
	destination_file = open(destination, 'wb')
	destination_file.write(source_file.read())
	destination_file.close()
	source_file.close()
	
def save_test_in_student_folders(test):
	
	students = queries.get_all_students()
	exercise = test.exercise
	
	for s in students:
		usr = s.username
		path = settings.MEDIA_ROOT + '/' + usr + '/' + exercise.name + '/'
		test_full_path =  path + test.path
		if not os.path.exists(path):
			os.makedirs(path)
		
		try:
			os.remove(path + t.path)
		except:
			pass
		dest = open(test_full_path, 'wb')
		aux = "'" + path + "'"
		if test.code.__contains__("from pexpect import *"):
			number = test.code.count('%')
			aux2 = number*(path,)
			dest.write((test.code % aux2) + '\n\n\n' + (configuration.TEST_APPEND_STUDENT_FOLDER % (test.name, aux)))
		else:
			dest.write(test.code + '\n\n\n' + configuration.TEST_APPEND_STUDENT_FOLDER % (test.name, aux))
		dest.close()
			
class Table_Delivered:
	"""Contains all necessary informations to the table of delivered exercises"""
	
	def __init__(self, exercise, submission, num_submissions, solved, errors, score, percentage):
		self.exercise = exercise
		self.submission = submission
		self.number_submissions = num_submissions
		self.last_submission_date = submission.date
		self.number_tests = exercise.number_tests
		self.was_solved = solved
		self.num_errors = errors
		self.score = score
		self.class_percentage = percentage
		if self.number_tests != 0:
			self.your_right = ((self.number_tests - errors)/float(self.number_tests))*100
		else:
			self.your_right = 0
			
class Student_Results:
	def __init__(self, student, exercise, num_submissions, submission, execution):
		self.student_name = student.username
		self.student_assistant = student.assistant.username
		self.number_submissions = num_submissions
		if not execution:
			self.errors_number = 0
			self.pass_number = 0
		else:
			self.errors_number = execution.errors_number
			self.pass_number = execution.pass_number
		self.number_tests = exercise.number_tests
		self.veredict = submission.veredict
		if submission.score:
			self.score = submission.score
		else:
			self.score = None
			
class Temp_Results:
	def __init__(self, student, submission, num_errors, num_failures, num_tests, log_errors):
		self.student = student
		self.submission = submission
		self.num_errors = num_errors
		self.num_pass = num_tests - (num_errors + num_failures)
		self.num_failures = num_failures
		self.num_tests = num_tests
		self.log_errors = log_errors
		
		
def student_exercises(student_id):
	informations = []
	solved = False
	score = 0.0
	errors = 0
	
	student = queries.get_student(student_id)
	exercises = queries.get_all_exercises()
	
	for ex in exercises:
		submission = None
		submissions = queries.get_submissions(ex.id, student_id)					
		try:
			submission = submissions.order_by('date').reverse()[0]
			execution = queries.get_last_execution(submission.id)
		except:
			execution = None
		
		if submission and (submission.veredict == 'Pass'):
			solved = True
			if execution:
				errors = execution.errors_number
			score = submission.score
		
		if submission:	
			date = submission.date
			percentage = calculate_correct_percentage(ex)
			d = Table_Delivered(ex, submission, submissions.count(), solved, errors, score, percentage)
			informations.append(d)
	return informations