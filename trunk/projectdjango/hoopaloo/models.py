# coding: utf-8

#Hoopaloo - Version 1.0 - 2008/2009
#Author: Mariana Romao do Nascimento - mariana@dsc.ufcg.edu.br
import datetime
from datetime import timedelta
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from hoopaloo import configuration
import util
import queries

class Actions_log(models.Model):
	"""This model storages a log of actions of users."""
	
	user = models.ForeignKey(User) # the user that realizes the action
	action = models.CharField(max_length=100) # the action realized
	date = models.DateTimeField() # the date
	
	def create_action(self, user, action, date):
		log = Actions_log()
		log.user = user
		log.action = action
		log.date = date
		return log
	
class Class(models.Model):
	"""This model represents a student class."""
	
	name = models.CharField(max_length=20) # The class name (for example: labprog1-t1)
	teacher = models.ForeignKey(User) # The teacher of class
	
	def create_and_save_class(self, name, teacher):
		myclass = Class()
		myclass.name = name
		myclass.teacher = teacher
		myclass.save()
		
	def __unicode__(self):
		return self.name
	
class Assistant(models.Model):
	"""Assistant is a profile with almost same privileges than a teacher"""
	
	user = models.OneToOneField(User)
	username = models.CharField(max_length=30)
	realized_login = models.BooleanField()

	def create_assistant(self, user, username):
		assistant = Assistant()
		assistant.user = user
		assistant.username = username
		assistant.realized_login = False
		return assistant
		

class Exercise(models.Model):
	"""An Exercise is registered by a teacher or by an assistant."""
	
	name = models.CharField(max_length=200, unique=True) # The name must be unique
	description = models.TextField() # The description of exercise
	available = models.BooleanField() # If the exercise is available to submissions
	owner = models.ForeignKey(User) # The creator of exercise
	date_availability = models.DateTimeField() # Date in which the exercise was available
	date_finish = models.DateTimeField() # Date in which the exercise will be unavailable
	number_tests = models.IntegerField() # Number of tests registereds to this exercise
	number_students_that_solved = models.IntegerField() # Number of students that solved the exercise
	mean_notes = models.FloatField() # Mean of notes of the students
	send_email_teacher = models.BooleanField() # If an email was sended to the teacher because this exercise. This will be necessary when a teacher registered an exercise and not register a test. Then, an email will be sended to the teacher in order to say that a student submit a solution, but are not tests
	
	def create_exercise(self, name, description, owner, available, date=None):
		from hoopaloo.util import get_time_unavailability, get_next_friday, Change_Availability
		
		exercise = Exercise()
		exercise.name = name
		exercise.description = description
		exercise.available = available
		exercise.owner = owner
		if available:
			exercise.date_availability = datetime.datetime.now()
	
		if date:
			exercise.date_finish = date 
		'''else:
			today = datetime.datetime.now()
			# if the teacher not specify a date of unavailability the default is the next friday
			exercise.date_finish = util.get_next_friday(today)'''
		
		exercise.number_tests = 0
		exercise.number_students_that_solved = 0
		exercise.mean_notes = 0.0
		exercise.send_email_teacher = False
		
		if exercise.available:
			try:
				t = get_time_unavailability(exercise.date_finish, exercise.date_availability)
				cron = Change_Availability(exercise.name, t)
				cron.init_cont()
			except:
				return None
		
		return exercise
		
	def __unicode__(self):
		return self.name

class Student(models.Model):
	"""A Student is a profile."""
	
	user = models.OneToOneField(User)
	username = models.CharField(max_length=30)
	assistant = models.ForeignKey(Assistant, blank=True) # The assistant that holds this student
	studentID = models.CharField(max_length=8, unique=True)
	student_class = models.ForeignKey(Class)
	number_submissions = models.IntegerField() # Number of submission realized by thsi student
	solved_exercises = models.IntegerField() # number of exercises that the student delivered and they were correct
	unsolved_exercises = models.IntegerField() # number of exercises that the student delivered but  they were not correct
	pending_exercises = models.IntegerField() # number of exercises that the student delivered but they are activity
	mean = models.FloatField() # Mean of notes
	undelivered_exercises = models.IntegerField() # number of exercises that the student don�t delivered
	submission_by_exercise = models.FloatField() # rate of submission divided by the number of exercises
	realized_login = models.BooleanField()
	
	def create_student(self, user, username, studentID, _class):
		st = Student()
		st.user = user
		st.username = username
		st.studentID = studentID
		st.student_class = queries.get_class_from_name(_class)
		st.number_submissions = 0
		st.solved_exercises = 0
		st.unsolved_exercises = 0
		st.pending_exercises = queries.get_number_available_exercises()
		st.undelivered_exercises = 0
		st.submission_by_exercise = 0
		st.mean = 0.0
		st.realized_login = False
		
		# creating the dir of student
		if not os.path.exists(settings.MEDIA_ROOT + '/' + username + '/'):
			os.makedirs(settings.MEDIA_ROOT + '/' + username + '/')
				
		return st
		
	def __unicode__(self):
		return self.username
		
class Submission(models.Model):
	"""A Submission is realized by a student in order to solve a exercise."""
	
	id_student = models.ForeignKey(Student)
	solution_file = models.FileField(max_length=300, upload_to='/uploads') # The path of solution file
	id_exercise = models.ForeignKey(Exercise)
	date = models.DateTimeField() # date in which the submission was realized
	file_length = models.IntegerField()
	was_executed = models.BooleanField() # true if the program was executed by tests
	veredict = models.CharField(max_length=30) # pass or fail
	score = models.FloatField(blank=True)
	comments = models.CharField(max_length=1000, blank=True)
	
	def create_submission(self, user, file, exercise, length):
		submission = Submission()
		submission.id_student = user
		submission.solution_file = file
		submission.id_exercise = exercise
		submission.file_length = length
		submission.date = datetime.datetime.now()
		submission.was_executed = False
		return submission
	
	def __unicode__(self):
		return self.id_student.username + ' - ' + self.id_exercise.name
		
class Test(models.Model):
	"""Test is a test case registered by teacher or assistants to be executed at the students' solutions."""
	
	name = models.CharField(max_length=200) # The name of test
	path = models.CharField(max_length=200) # The name of test file (has the extension .py)
	code = models.TextField() # The code as it was registered, the original code without system appends
	creation_date = models.DateTimeField('Creation Date')
	owner = models.ForeignKey(User)
	exercise = models.ForeignKey(Exercise) # the exercise related to this test
	locked = models.BooleanField()
	
	def create_test(self, owner, exercise, code):
		new_test = Test()
		new_test.name = 'Teste_' + exercise.name
		new_test.code = code
		new_test.creation_date = datetime.datetime.now()
		new_test.owner = owner
		new_test.exercise = exercise
		new_test.path = new_test.name + '.py'
		new_test.locked = False
		
		return new_test
		
	def __unicode__(self):
		return self.name
		
class UnderTest(models.Model):
	"""Represents a test under test, i.e., a test under edition by teachers or assistants."""
	
	name = models.CharField(max_length=200) # The name of test
	path = models.CharField(max_length=200) # The name of test file (has the extension .py)
	code = models.TextField() # The code as it was registered, the original code without system appends
	creation_date = models.DateTimeField('Creation Date')
	owner = models.ForeignKey(User)
	exercise = models.ForeignKey(Exercise) # the exercise related to this test

	def create_test(self, owner, exercise, code):
		new_test = UnderTest()
		new_test.name = 'UnderTest_' + exercise.name
		new_test.code = code
		new_test.creation_date = datetime.datetime.now()
		new_test.owner = owner
		new_test.exercise = exercise
		new_test.path = new_test.name + '.py'

		return new_test
		
	def __unicode__(self):
		return self.name
		
class Execution(models.Model):
	"""An Execution is the result of the execution of a test upon an exercise."""
	
	id_submission = models.ForeignKey(Submission)
	id_student = models.ForeignKey(Student)
	id_test = models.ForeignKey(Test) # The test file that was executed
	errors_number = models.IntegerField() # Number of errors and failures of a test
	pass_number = models.IntegerField() # Number of tests that passed
	date = models.DateTimeField()
	log_errors = models.CharField(max_length=5000) # The string result of execution, has details of execution
	errors_to_student = models.CharField(max_length=2000) # The sring result of execution registered by teacher
	was_success = models.BooleanField() # If the execution has sucess or not
	loop = models.BooleanField() # If the program entered in inifinite loop
	
# SIGNALS	
from django.db.models.signals import post_save, pre_delete, pre_save
			
def execution_saved(sender, instance, signal, *args, **kwargs):
	"""This signal is called always an execution is saved in database. It recovers the informations
	of execution and creates a result."""
	
	id_st = instance.id_student.id
	student = queries.get_student(id_st)
	submission = queries.get_submission(instance.id_submission.id)
	id_ex = queries.get_exercise(submission.id_exercise.id)
	errors_number = instance.errors_number
	pass_number = instance.pass_number
	num_submissions = queries.get_number_student_submissions(submission.id_exercise, id_st)
	if (errors_number == 0) and (not instance.loop):
		veredict = 'Pass'
	else:
		veredict = 'Fail'
	#TODO ACHO QUE EH AQUI O PROFESSOR VAI SER AVISADO DO RESULTADO DE SUBMISSÔES
	
def create_or_update_test(sender, instance, signal, *args, **kwargs):
	"""This function is called when a test is modified or is created. It execute the students programs."""
	
	if not instance.locked:
		from hoopaloo.util import notify_students
		students = queries.get_all_students()
		exercise = instance.exercise
		test = instance
		from hoopaloo.Tester import Tester
			
		for s in students:
			tester = Tester(s, test, exercise) 
			tester.execute_test()
			
	#TODO nao notificar ninguem por enquanto
	#notify_students(students, test, id_exercise)

def pre_delete_exercise(sender, instance, signal, *args, **kwargs):
	"""This function is invoked when an exercise is deleted. 
	It removes the files associated to this exercise and update some student informations."""
	
	test = queries.get_consolidated_test(instance.id)
	os.remove(settings.MEDIA_ROOT + '/tests/' + test.path)
	try:
		os.remove(settings.MEDIA_ROOT + '/tests/' + configuration.BACKUP_TEST_NAME + '_'+ instance.name + '.py')
	except:
		pass
	students = queries.get_all_students()
	for s in students:
		os.remove(settings.MEDIA_ROOT + '/' + s.username + '/' + instance.name + '/' + test.path)
		if instance.available == True:		
			number = queries.get_number_available_exercises()
			if number > 0:
				s.pending_exercises = number - 1
		else:
			try:
				submission = queries.get_last_submission(instance.id, s.id)
				# if the student solved this exercise then decrement solved exercises
				if submission.veredict == 'Pass' and instance.available == False:
					number = queries.get_number_solved_exercises()
					if number > 0:
						s.solved_exercises = number - 1
				# if the student not solved this exercise then decrement unsolved exercises
				if submission.veredict == 'Fail' and instance.available == False:
					number = queries.get_number_unsolved_exercises()
					if number > 0:
						s.unsolved_exercises =  - 1
			except:
				# the student not submit a solution for this exercise
				number = queries.get_undelivered_exercises()
				if number > 0:
					s.undelivered_exercises = number - 1
		
		num_submissions = queries.get_number_total_student_submissions(s.id) - queries.get_number_student_submissions(instance.id, s.id)
		num_exercises = queries.get_number_exercises() - 1
		s.submission_by_exercise = num_submissions/num_exercises
		s.save()
		
		
def pre_delete_student(sender, instance, signal, *args, **kwargs):
	"""This function is invoked when a student is deleted. It removes the student files and folder and update 
	exercise settings."""
	
	# Updating settings of exercises
	exercise_results = []
	exercises = Exercise.objects.all()
	for ex in exercises:
		try:
			submission = queries.get_last_submission(ex.id, instance.id)
			if s.veredict == 'Pass':
				number = queries.number_students_that_solved()
				if number > 0:
					ex.number_students_that_solved =  number - 1
			
			#TODO COLOCAR ESSA ATUALIZAÇÂO DE EXERCICIO EM OUTRO LUGAR. AQUI NAO DAH CERTO
			exercise.mean_notes = util.mean(exercise_results)
			exercise.save()
		except:
			pass
	
	# Deleting files and folders of student
	for root, dirs, files in os.walk(settings.MEDIA_ROOT + '/' + instance.username, topdown=False):
		for f in files:
			os.remove(os.path.join(str(root), str(f)))
		for d in  dirs:
			try:
				os.removedirs(os.path.join(str(root), str(d)))
			except:
				pass
	
def pre_save_exercise(sender, instance, signal, *args, **kwargs):
	"""This functions is invoked before an exercise to be saved. It add one more exercise pending to students if this exercise is available."""
	
	try:
		queries.get_exercise(instance.id)
	except:
		if instance.available:
			students = queries.get_all_students()
			for s in students:
				s.pending_exercises = queries.get_number_available_exercises() + 1
				s.save()		
	
def post_save_exercise(sender, instance, signal, *args, **kwargs):
	
	try:
		# if this exercise exists and only is being updated
		test = queries.get_consolidate_test(instance.id)
	except:
		name_test = 'Test_' + instance.name.replace(".", "_")
		test = Test().create_test(instance.owner, instance, configuration.TEST_DEFAULT_CODE % name_test)
		try:
			# creating backup file
			util.copy_file(settings.MEDIA_ROOT + '/tests/' + test.path, settings.MEDIA_ROOT + '/tests/' + configuration.BACKUP_TEST_NAME + '_' + exercise.name + '.py')
			os.remove(settings.MEDIA_ROOT + '/tests/' + t.path)
		except:
			pass
			
		path_tests = settings.MEDIA_ROOT + '/tests/' + test.path
		dest = open(path_tests, 'wb')
		dest.write(test.code + configuration.TEST_APPEND)
		dest.close()
			
		util.save_test_in_student_folders(test)
		test.save()	
		
# The connection between the signals and the functions
post_save.connect(execution_saved, sender=Execution, dispatch_uid='post_save.execution_saved')
post_save.connect(create_or_update_test, sender=Test, dispatch_uid='post_save.create_or_update_test')
pre_save.connect(pre_save_exercise, sender=Exercise, dispatch_uid='pre_save.pre_save_exercise')
post_save.connect(post_save_exercise, sender=Exercise, dispatch_uid='post_save.post_save_exercise')
pre_delete.connect(pre_delete_student, sender=Student, dispatch_uid='pre_delete.pre_delete_student')
pre_delete.connect(pre_delete_exercise, sender=Exercise, dispatch_uid='pre_delete.pre_delete_exercise')