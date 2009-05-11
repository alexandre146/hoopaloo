# coding: utf-8
from django.test import TestCase
from django.test.client import Client
from datetime import datetime, date, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from hoopaloo_test.models import Exercise, Student, Assistant, Submission, Exercise, Execution, Test, Class
from hoopaloo_test import forms
from hoopaloo_test.util import *

class MyTestCase(TestCase):
	
	def setUp(self):
		self.client = Client()
		
	def tearDown(self):
		pass
	
	def aux_create_assistant(self):
		user = User.objects.create_user('assistant', 'assistant@assistant.com', 'assistant_password')
		user.first_name = 'Assistant'
		user.last_name = 'Test'
		user.save()
		
		a = Assistant().create_assistant(user, 'assistant')
		a.save()
	
	def aux_create_exercise(self, num=None):
		try:
			user = User.objects.create(username='test', password='test', email='test@test.com')
		except:
			user = User.objects.get(username='test')
		d = datetime(2009, 12, 31, 12, 00, 0)
		if num != None:
			ex = Exercise().create_exercise('Ex_test'+str(num), 'Description Test', user, True, d)
		else:
			ex = Exercise().create_exercise('Ex_test', 'Description Test', user, True, d)
		ex.save()

	def aux_create_class(self):
		user = User.objects.create_user('superuser', 'superuser@superuser.com', 'superuser_password')
		user.first_name = 'Superuser'
		user.last_name = 'Test'
		user.save()
		
		st_class = Class().create_and_save_class('turma', user)

	def aux_create_student(self):
		self.aux_create_class()
		
		user = User.objects.create_user('student_test', 'student_test@test.com', generate_aleatory_password())
		user.first_name = 'Student'
		user.last_name = 'Test'
		user.save()
			
		st = Student().create_student(user, 'student_test', 10000001, 'turma')
		st.assistant = Assistant.objects.get(username='assistant')
		st.save()
		
	def aux_create_submission(self, exercise_name):
		st = Student.objects.get(username="student_test")
		ex = Exercise.objects.get(name=exercise_name)
		filename = 'C:\\Documents and Settings\\mariana\Desktop\\outrasoma.py'
		
		submission = Submission().create_submission(st, filename, ex, 100)
		submission.score = 0.0
		submission.veredict = ""
		submission.save()
		
	def Oktest_create_exercise(self):
		self.aux_create_exercise(5)
		
		exercise = Exercise.objects.get(name='Ex_test5')
		self.assertEquals(exercise.name, 'Ex_test5')
		self.assertEquals(exercise.description, 'Description Test')
		self.assertTrue(exercise.available)
		
	def OKtest_register_assistant(self):
		self.aux_create_assistant()
		
		assistant = Assistant.objects.get(username='assistant')
		self.assertEquals(assistant.username, 'assistant')
		self.assertEquals(assistant.user.email, 'assistant@assistant.com')
		self.assertEquals(assistant.user.first_name, 'Assistant')
		self.assertEquals(assistant.user.last_name, 'Test')

	def Oktest_register_student(self):
		self.aux_create_assistant()
		
		student = Student.objects.get(pk=1)
		self.assertEquals(student.username, 'student_test')
		self.assertEquals(student.user.email, 'student_test@test.com')
		self.assertEquals(int(student.studentID), 10000001)
		self.assertEquals(student.user.first_name, 'Student')
		self.assertEquals(student.user.last_name, 'Test')
				
	def OKtest_create_submission(self):
		
		self.aux_create_assistant()
		self.aux_create_student()
		self.aux_create_exercise()
		self.aux_create_submission('Ex_test')
		
		student = Student.objects.get(username='student_test')
		number_ex = float(Exercise.objects.all().count())
		#doing updtade in student
		student.number_submissions += 1
		student.submission_by_exercise = student.number_submissions/number_ex
		student.save()

		self.assertEquals(student.number_submissions, 1)
		self.assertEquals(student.submission_by_exercise, 1)
		
	def OKtest_username(self):
		user = User.objects.create_user('student_test5', 'student_test5@test.com', generate_aleatory_password())
		user.save()

		self.assertFalse(isValidUsername('student_test5'))
		self.assertTrue(isValidUsername('mariana'))
		print 'username_test'
		
	def OKtest_email(self):
		valid_email = 'mari.ufcg@gmail.com'
		invalid_email = 'mari.com'
		
		self.assertTrue(isValidEmail(valid_email))
		self.assertFalse(isValidEmail(invalid_email))
		print 'email_test'
		
	def OKtest_studentID(self):
		valid_id = 12345678
		invalid_id = 123
		invalid_id_2 = "invalid"
		
		self.assertTrue(isValidStudentID(valid_id))
		self.assertFalse(isValidStudentID(invalid_id))
		self.assertFalse(isValidStudentID(invalid_id_2))
		print 'studentID_test'
		
	def Oktest_cenario_one(self):
		self.aux_create_assistant()
		# saving a new student
		self.aux_create_student()		
		st = Student.objects.get(username="student_test")
		# verifyng student data
		self.assertEquals(st.number_submissions, 0)
		self.assertEquals(st.solved_exercises, 0)
		self.assertEquals(st.unsolved_exercises, 0)
		self.assertEquals(st.pending_exercises, 0)
		self.assertEquals(st.mean, 0)
		self.assertEquals(st.undelivered_exercises, 0)
		self.assertEquals(st.submission_by_exercise, 0)
		
		# saving two new exercises
		self.aux_create_exercise(1)
		self.aux_create_exercise(2)
		
		# simulating a submission of student_test2 to exercise ex1
		# first submission
		self.aux_create_submission("Ex_test1")
		st.number_submissions += 1
		st.submission_by_exercise = st.number_submissions/len(Exercise.objects.all())
		st.save()
		#second submission
		self.aux_create_submission("Ex_test1")
		st.number_submissions += 1
		st.submission_by_exercise = st.number_submissions/len(Exercise.objects.all())
		st.save()
		# simulating a submission of student_test2 to exercise ex2
		# first submission
		self.aux_create_submission("Ex_test2")
		st.number_submissions += 1
		st.submission_by_exercise = st.number_submissions/len(Exercise.objects.all())
		st.save()
		#second submission
		self.aux_create_submission("Ex_test2")
		st.number_submissions += 1
		st.submission_by_exercise = st.number_submissions/len(Exercise.objects.all())
		st.save()
		#thrird submission
		self.aux_create_submission("Ex_test2")
		st.number_submissions += 1
		st.submission_by_exercise = st.number_submissions/len(Exercise.objects.all())
		st.save()
		#fourth submission
		self.aux_create_submission("Ex_test2")
		st.number_submissions += 1
		st.submission_by_exercise = st.number_submissions/len(Exercise.objects.all())
		st.save()			
					
		student = Student.objects.get(pk=st.id)
		# verifyng student data
		self.assertEquals(student.number_submissions, 6)
		self.assertEquals(student.submission_by_exercise, 3.0)
		
# TESTING UTIL FUNCTIONS 

	def Oktest_generate_aleatory_password(self):
		password1 = generate_aleatory_password()
		password2 = generate_aleatory_password()
		self.assertEquals(6, len(password1))
		self.assertEquals(6, len(password2))
		self.assertNotEquals(password1, password2)

	def Oktest_listToString(self):
		my_list1 = [" ", " ", " "]
		self.assertEquals(" \n \n \n", listToString (my_list1))
		
		my_list2 = [1, "Nothing"]
		self.assertEquals("1\nNothing\n", listToString, my_list2)
		
		my_list3 = []
		self.assertEquals("", listToString(my_list3))
		
		my_list4 = ["All"]
		self.assertEquals("All\n", listToString(my_list4))
		
		my_list5 = [None]
		self.assertEquals("", listToString(my_list5))
		
	def Oktest_isValidUsername(self):
		user1 = User.objects.create(username='user1', password='user1', email='user1@test.com')
		self.assertFalse(isValidUsername("user1"))
		self.assertTrue(isValidUsername("username"))
		self.assertFalse(isValidUsername(""))
		self.assertFalse(isValidUsername(None))
		self.assertFalse(isValidUsername(" "))
		self.assertFalse(isValidUsername("&%$#@"))
		self.assertFalse(isValidUsername("user#$@"))
		self.assertTrue(isValidUsername("user43"))
		self.assertFalse(isValidUsername("65643"))
		
	def Oktest_isValidEmail(self):
		self.assertTrue(isValidEmail("mariana@dsc.ufcg.edu.br"))
		self.assertFalse(isValidEmail(""))
		self.assertFalse(isValidEmail(None))	
		self.assertFalse(isValidEmail("&¨%$$#@"))
		self.assertFalse(isValidEmail(" "))
		self.assertFalse(isValidEmail("mariana.dsc.ufcg.edu.br"))
		self.assertFalse(isValidEmail("mariana@"))
		
	def Oktest_isValidStudentID(self):
		self.assertTrue(isValidStudentID("12345678"))
		self.assertFalse(isValidStudentID("mnfbnmbfn"))
		self.assertFalse(isValidStudentID(" "))
		self.assertFalse(isValidStudentID(""))
		self.assertFalse(isValidStudentID(None))
		
	def Oktest_get_next_friday(self):
		td = date.today()
		friday = td + timedelta(4)
		self.assertEquals(friday, get_next_friday(td))	
		
		day1 = date(2009, 05, 18)
		day2 = date(2009, 05, 22)
		self.assertEquals(day2, get_next_friday(day1))
		
		day3 = date(2009, 02, 28)
		day4 = date(2009, 03, 06)
		self.assertEquals(day4, get_next_friday(day3))
		
	
# --------------------------- TESTS FOR VIEWS --------------------------- #

	def OKtest_login(self):
		response = self.client.get("/hoopaloo_test/login/")
		self.assertEquals(response.status_code, 200)
		response = self.client.post("/hoopaloo_test/login/", {'username':'professor', 'password':'professor'})
		self.assertEquals(response.status_code, 200)
		response = self.client.post("/hoopaloo_test/login/", {'username':'professor', 'password':'senha'})
		self.assertContains(response, 'Invalid Access', count=None, status_code=200)
		
	def Oktest_register_assistant(self):
		from django.contrib import auth
		user = auth.authenticate(username='professor', password='professor')
		response = self.client.get("/hoopaloo_test/register_assistant/")
		self.assertEquals(response.status_code, 200)
		
