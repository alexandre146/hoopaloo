# coding: utf-8

#Hoopaloo - Version 1.0 - 2008/2009
#Author: Mariana Romao do Nascimento - mariana@dsc.ufcg.edu.br

import smtplib
import random
import sha
import os
import re
from datetime import date, datetime, timedelta
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from hoopaloo import configuration



def generate_aleatory_password():
	"""Generates a new password aleatorily"""
	
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
		User.objects.get(username=field_data)
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
	
	# APAGAR DEPOIS
	msg = 'Your program was updated sucessfully. Check your code submission in table bellow.'	
	msgs.append(msg)
	return True, msgs
	#
	
	if result == None:
		msg = configuration.EXECUTION_AFTER
		msgs.append(msg)
		return None, msgs
	else:
		submission = Submission.objects.filter(id_student=result.id_student.id, id_exercise=result.id_exercise.id).order_by('date').reverse()[0]
		execution = Execution.objects.filter(id_student=result.id_student.id, id_submission=submission.id).order_by('date').reverse()[0]
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
			
def notify_students(students, test, id_ex):
	"""Notify the students about the result of execution tests."""
	
	from hoopaloo.models import Submission, Result
	test_creation_date = test.creation_date
	for s in students:
		if len(Submission.objects.filter(id_student=s.id, id_exercise=id_ex).order_by('date')) != 0:
			last_submission = Submission.objects.filter(id_student=s.id, id_exercise=id_ex).order_by('date')[0]
			if last_submission.date <= test_creation_date:
				result = Result.objects.get(id_student=s.id, id_exercise=id_ex)
				veredict, message = make_message_student(result)
				
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
	
	from hoopaloo.models import Student, Result
	students = Student.objects.all()
	for s in students:
		try:
			result = Result.objects.get(id_exercise = exercise.id, id_student=s.id)
			if result.veredict == 'Pass':
				s.solved_exercises = s.solved_exercises + 1
			else:
				s.unsolved_exercises = s.unsolved_exercises + 1
		except:
			s.undelivered_exercises = s.undelivered_exercises + 1
		s.pending_exercises = s.pending_exercises - 1
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
		exercise = Exercise.objects.get(name=self.exercise_name)
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
	
	from hoopaloo.models import Result
	result_p = []
	for p in percentual_list:
		num = 0
		for s in students:
			try:
				result = Result.objects.get(id_exercise=exercise.id, id_student=s.id)
				aux = (result.pass_number * 100) / exercise.number_tests
				if aux == p:
					num += 1
			except:
				if p == 0:
					num += 1
		element = MyTuple(p, num*100/len(students) )
		result_p.append(element)
	return result_p

def calculate_note_percentual(percentual_list, results, exercise):
	"""Returns a list in which each element has a percentual.
	This percentual is a percent of note. For example: 20% of class received note between 8 and 9."""
	
	result_p = []
	count = 0
	for p in percentual_list:
		num = 0
		for r in results:
			if r.note <= p[0] and r.note >= p[1]:
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
		if r.note != None:
			sum += r.note
			count +=1
	if len(results) != 0:
		mean = sum/count
	return mean
	
	
def calculate_mean_student(student):
	"""Calculates the mean of note of a student"""
	
	from hoopaloo.models import Result
	results = Result.objects.filter(id_student=student.id)
	return mean(results)
	
def calculate_mean(exercise):
	"""Calculates the mean of notes of an exercise"""
	
	from hoopaloo.models import Result
	results = Result.objects.filter(id_exercise=exercise.id)
	return mean(results)
	
def get_students_percent(percent, id_ex):
	"""Returns the students that passed in percentual (percent) of right tests"""
	
	from hoopaloo.models import Exercise, Student, Result
	students = Student.objects.all()
	exercise = Exercise.objects.get(pk=id_ex)
	st_percent = []
	for s in students:
		aux = 0
		try:
			result = Result.objects.get(id_exercise=id_ex, id_student=s.id)
			aux = (result.pass_number * 100) / exercise.number_tests
			if aux == int(percent):
				st_percent.append(s)
		except:
			if int(percent) == aux :
				st_percent.append(s)

	return st_percent

def get_students_score_percent(index, id_exercise):
	"""Returns the students that has a specific note (referenced by index)"""
	
	from hoopaloo.models import Exercise, Student, Result
	students = Student.objects.all()
	exercise = Exercise.objects.get(pk=id_exercise)
	st_percent = []

	score = configuration.PERCENT_OF_SCORE[index]
	score1 = note[1]
	score2 = note[0]

	for s in students:
		aux = 0
		try:
			result = Result.objects.get(id_exercise=exercise.id, id_student=s.id)
			if (result.note >= float(score1) and result.note <= float(score2)):
				st_percent.append(s)
		except:
			pass
	return st_percent
	
def calculate_correct_percentage(exercise):
	"""Calculate the percentage of right tests of all students to an specific exercise"""
	
	from hoopaloo.models import Student, Result
	students = Student.objects.all()
	percent = 0 
	for s in students:
		try:
			result = Result.objects.get(id_exercise=exercise.id, id_student=s.id)
			if result.veredict == 'Pass':
				percent +=1 
		except:
			pass
	return (percent*100)/students.count()
	
def is_assistant(user):
	if user.is_superuser:
		return False
	return True
	
def get_available_exercises(user):
	from hoopaloo.models import Exercise
	available = Exercise.objects.filter(available=True)
	student = user.get_profile()
	undelivered = []
	for ex in available:
		try:
			# tem um erro aqui e nao sei qual eh, nao pega a submissao, mesmo que ela exista
			submited = Submission.objects.get(id_student=student.id, id_exercise=ex.id)
		except:
			undelivered.append(ex)
	return undelivered	
		
def delete_association(student_id):
	from hoopaloo.models import Student, Assistant
	
	student = Student.objects.get(pk=student_id)
	assistant = Assistant.objects.get(pk=student.assistant.id)
	student.assistant = Assistant.objects.get(username='-')
	student.save()
	
def add_note_and_comments(comments, note, exercise, submission):
	from hoopaloo.models import Result, Student
	result = Result.objects.get(id_exercise=exercise.id,id_student=submission.id_student.id)
	result.comments = comments
	has_error = False
	error = ''
	try:
		n = int(note)
	except:
		try:
			n = float(note)
		except:
			error = configuration.ADD_NOTE_ERROR
			has_error = True

	if n > 10 or n < 0:
		error = configuration.ADD_NOTE_ERROR_2
	else:
		result.note = n
		result.save()
		exercise.mean_notes = calculate_mean(exercise)
		exercise.save()
		student = Student.objects.get(pk=submission.id_student.id)
		student.mean = calculate_mean_student(student)
		student.save()
	return has_error, error
		
def students_solved(exercise):
	from hoopaloo.models import Result
	
	count = 0
	results = Result.objects.filter(id_exercise=exercise.id)
	for r in results:
		if r.veredict == 'Pass':
			count += 1
	return count
	
def update_availability(id_exercise):
	from hoopaloo.models import Exercise, Student
	
	ex = Exercise.objects.get(pk=id_exercise)
	if ex.available == True:
		available = False
		update_students(ex)
		ex.number_students_that_solved = students_solved(ex)
	else:
		available = True
		ex.date_availability = datetime.today()
		students = Student.objects.all()
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
	available = Exercise.objects.filter(available=True).order_by('date_finish').reverse()
	delivered = []
	for ex in available:
		try:
			submited = Submission.objects.filter(id_student=student_id, id_exercise=ex.id).order_by('date').reverse()
			result = Result.objects.get(id_exercise = ex.id, id_student=student_id)
			if result.veredict == 'Pass':
				solved = True
			else:
				solved = False
			date = submited[0].date
			percentage = calculate_correct_percentage(ex)
			d = Table_Delivered(ex, result.num_submissions, date, ex.number_tests, solved, result.errors_number, result.note, percentage)
			delivered.append(d)
		except:
			pass
	return delivered
		
def copy_test_files(student):
	from hoopaloo.models import Test, Exercise
	exercises = Exercise.objects.all()
	for e in exercises:
		path_student = settings.MEDIA_ROOT + '/' + student.username + '/' 
		try:
			test = Test.objects.get(exercise=e.id)
			student_test = open(path_student + test.path, 'wb')
			file_test = open(settings.MEDIA_ROOT + '/tests/' + test.path, 'rb')
			lines = file_test.readlines()
			contend = ''
			for l in lines:
				contend += l
			student_test.write(contend + configuration.TEST_APPEND_STUDENT_FOLDER % path_student)
			student_test.close()
			file_test.close()
		except:
			# have not test for this exercise
			pass
		
def copy_test_files(student):
	"""Copy all test files in the student folder"""
	
	from hoopaloo.models import Test, Exercise
	exercises = Exercise.objects.all()
	for e in exercises:
		path_student = settings.MEDIA_ROOT + '/' + student.username + '/' 
		try:
			test = Test.objects.get(exercise=e.id)
			student_test = open(path_student + test.path, 'wb')
			file_test = open(settings.MEDIA_ROOT + '/tests/' + test.path, 'rb')
			lines = file_test.readlines()
			contend = ''
			for l in lines:
				contend += l
				
			if contend.__contains__("from pexpect import *"):
				number = contend.count('%')
				aux = number*(path_student,)
				student_test.write((contend % aux ) + configuration.TEST_APPEND_STUDENT_FOLDER % path_student)
			else:
				student_test.write(contend  + configuration.TEST_APPEND_STUDENT_FOLDER % path_student)
			
			student_test.close()
			file_test.close()
			
		except:
			# have not test for this exercise
			pass

		
def change_test(test, contend):
	from hoopaloo.models import Student, Exercise
	
	exercise = Exercise.objects.get(pk=test.exercise.id)
	
	# exists a copy of test file is in '/tests/'
	old_file_path = settings.MEDIA_ROOT + '/tests/' + test.path
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
	
	# save the new conted of test
	path_tests = settings.MEDIA_ROOT + '/tests/' + test.path
	dest = open(path_tests, 'wb')
	
	dest.write(contend + configuration.TEST_APPEND)
	dest.close()
			
	students = Student.objects.all()
	# in this loop, delete the old test files that were in students' folders
	for s in students:
		usr = s.username
		path_student = settings.MEDIA_ROOT + '/' + usr + '/'
		old_file_students_path = path_student + test.path
		os.remove(old_file_students_path)
		
		test_full_path =  path_student + test.path
		if not os.path.exists(path_student):
			os.makedirs(path_student)
		dest = open(test_full_path, 'wb')
		if contend.__contains__("from pexpect import *"):
			number = contend.count('%')
			aux = number*(path_student,)
			dest.write((contend % aux) + (configuration.TEST_APPEND_STUDENT_FOLDER % path_student))
		else:
			dest.write(contend + configuration.TEST_APPEND_STUDENT_FOLDER % path_student)
		dest.close()
		
	
def create_datetime(d):

	pieces = d.split(" ")
	date = pieces[0]
	time = pieces[1]
	year, month, day = date.split("-")
	hour, minutes = time.split(":")
	
	return datetime(int(year), int(month), int(day), int(hour), int(minutes))
	
	
def get_path_to_download(student, submissions):
	tuples =[]
	for s in submissions:
		path_download = student.username + '/' + s.solution_file.name.split('/')[-1]
		tuples.append(MyTuple(s,path_download))
	return tuples
	
def remove_acentuation(code):
	f = open('/home/mariana/www/Debug.txt', 'wb')
	f.write(code)
	
	word = code.replace("á", "a")
	word = word.replace("Á", "A")
	word = word.replace("é", "e")
	word = word.replace("É", "E")
	word = word.replace("Í", "I")
	word = word.replace("í", "i")
	word = word.replace("Ó", "O")
	word = word.replace("ó", "o")
	word = word.replace("ú", "u")
	word = word.replace("Ú", "U")
	word = word.replace("Ç", "C")
	word = word.replace("ç", "c")
	word = word.replace("õ", "o")
	word = word.replace("Õ", "O")
	word = word.replace("Ã", "A")
	word = word.replace("ã", "a")	
	word = word.replace("à", "a")	
	
	f.write(word)
	f.close()
	return word	

def save_test_in_student_folders(test):
	from hoopaloo.models import Student
	
	students = Student.objects.all()
	exercise = test.exercise
	
	for s in students:
		usr = s.username
		path = settings.MEDIA_ROOT + '/' + usr + '/' + exercise.name + '/'
		test_full_path =  path +test.path
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
			dest.write((test.code % aux2) + (configuration.TEST_APPEND_STUDENT_FOLDER % aux))
		else:
			dest.write(test.code + configuration.TEST_APPEND_STUDENT_FOLDER % aux)
		dest.close()
	
def code(lines):
	"""Receive a list of lines of code and convert it to Line_Code in order to maintains the format"""
	
	code = []
	count = 0
	for line in lines:
		if str(line).count('\t') == 0:
			code.append(Line_Code(str(line), 0))
		elif str(line).count('\t') == (count + 1):
			code.append(Line_Code(str(line), 1))
		elif str(line).count('\t') == (count - 1):
			code.append(Line_Code(str(line), 2))
			count -= 1
		elif str(line).count('\t') == count:
			code.append(Line_Code(str(line), 0))
		print code[len(code)-1]
	for n in range(count):
		code.append(Line_Code("", 3))
	return code
	
		
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