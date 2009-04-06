# coding: utf-8
from django.test import TestCase
from django.test.client import Client
from django.utils import simplejson as json
from datetime import date
from django.conf import settings
from django.contrib.auth.models import User
from hoopaloo.models import Exercise, Student, Assistant, Submission, Exercise, Execution, Test
from hoopaloo import forms
from hoopaloo.util import generate_aleatory_password, isValidUsername, isValidEmail, isValidStudentID

class MyTestCase(TestCase):
	
	def setUp(self):
		self.client = Client()
		
	def tearDown(self):
		pass
	
	def test_exercise(self):
		user = User.objects.create(username='test', password='test', email='test@test.com')
		
		ex = Exercise().create_exercise('Ex_test5', 'Description Test', user, True)
		ex.save()
		
		exercise = Exercise.objects.get(name='Ex_test5')
		self.assertEquals(exercise.name, 'Ex_test5')
		self.assertEquals(exercise.description, 'Description Test')
		self.assertTrue(exercise.available)
		
		
	def test_register_assistant(self):
		
		user = User.objects.create_user('assistant', 'assistant@assistant.com', 'assistant_password')
		user.first_name = 'Assistant'
		user.last_name = 'Test'
		user.save()
		
		a = Assistant().create_assistant(user, 'assistant')
		a.save()
		
		assistant = Assistant.objects.get(username='assistant')
		self.assertEquals(assistant.username, 'assistant')
		self.assertEquals(assistant.user.email, 'assistant@assistant.com')
		self.assertEquals(assistant.user.first_name, 'Assistant')
		self.assertEquals(assistant.user.last_name, 'Test')
		print 'register_assistant_test'

		
	#TODO  ver isso, como ajeitar a criacao das tabelas para que de certo isso
	def test_register_student(self):
		u = User.objects.create_user('assistant2', 'assistant@assistant.com', 'assistant_password')
		u.first_name = 'Assistant'
		u.last_name = 'Test'
		u.save()
		
		a = Assistant().create_assistant(u, 'assistant2')
		a.save()
	
	
		user = User.objects.create_user('student_test', 'student_test@test.com', generate_aleatory_password())
		user.first_name = 'Student'
		user.last_name = 'Test'
		user.save()
		
		st = Student().create_student(user, 'student_test', 10000001)
		st.assistant = Assistant.objects.get(username='assistant2')
		st.save()
		
		student = Student.objects.get(pk=1)
		self.assertEquals(student.username, 'student_test')
		self.assertEquals(student.user.email, 'student_test@test.com')
		self.assertEquals(int(student.studentID), 10000001)
		self.assertEquals(student.user.first_name, 'Student')
		self.assertEquals(student.user.last_name, 'Test')
		print 'register_student_test'
	
	def test_create_exercise(self):
		user = User.objects.create_user('student_test2', 'student_test2@test.com', generate_aleatory_password())
		user.save()
		
		ex = Exercise().create_exercise('Ex_test', 'Description Test', user, True)
		ex.save()
		
		exercise = Exercise.objects.get(name='Ex_test')
		self.assertEquals(exercise.name, 'Ex_test')
		self.assertEquals(exercise.description, 'Description Test')
		self.assertTrue(exercise.available)
		self.assertEquals(exercise.owner.id, user.id)
		print 'create_exercise_test'
		
	def test_create_test(self):
		user = User.objects.create_user('student_test3', 'student_test2@test.com', generate_aleatory_password())
		user.save()
		
		ex = Exercise().create_exercise('Ex_test2', 'Description Test', user, True)
		ex.save()
	
		
		test = Test().create_test('MyTest', user, ex)
		test.save()
		
		t = Test.objects.get(name='MyTest')
		self.assertEquals(t.name, 'MyTest')
		self.assertEquals(t.owner.id, user.id)
		self.assertEquals(t.path, 'MyTest.py')
		self.assertEquals(t.exercise.name, 'Ex_test2')
		print 'create_test_test'
		
	def test_create_submission(self):
		
		u = User.objects.create_user('assistant3', 'assistant@assistant.com', 'assistant_password')
		u.first_name = 'Assistant'
		u.last_name = 'Test'
		u.save()
		
		a = Assistant().create_assistant(u, 'assistant3')
		a.save()
		
		user = User.objects.create_user('student_test4', 'student_test2@test.com', generate_aleatory_password())
		user.save()
		st = Student().create_student(user, 'student_test4', 10000002)
		st.assistant = Assistant.objects.get(username='assistant3')
		st.save()
		
		ex = Exercise().create_exercise('Ex_test2', 'Description Test', user, True)
		ex.save()
		
		ex = Exercise.objects.get(name='Ex_test2')
		filename = 'C:\\Documents and Settings\\mariana\Desktop\\outrasoma.py'
		
		submission = Submission().create_submission(st, filename, ex, 100)
		submission.save()

		student = Student.objects.get(username='student_test4')
		
		number_ex = float(Exercise.objects.all().count())
		#doing updtade in student
		student.number_submissions += 1
		student.submission_by_exercise = student.number_submissions/number_ex
		student.save()

		self.assertEquals(student.number_submissions, 1)
		self.assertEquals(student.submission_by_exercise, 1)
	
		print 'create_submission_test'
		
	def test_username(self):
		user = User.objects.create_user('student_test5', 'student_test5@test.com', generate_aleatory_password())
		user.save()

		self.assertFalse(isValidUsername('student_test5'))
		self.assertTrue(isValidUsername('mariana'))
		print 'username_test'
		
	def test_email(self):
		valid_email = 'mari.ufcg@gmail.com'
		invalid_email = 'mari.com'
		
		self.assertTrue(isValidEmail(valid_email))
		self.assertFalse(isValidEmail(invalid_email))
		print 'email_test'
		
	def test_studentID(self):
		valid_id = 12345678
		invalid_id = 123
		invalid_id_2 = "invalid"
		
		self.assertTrue(isValidStudentID(valid_id))
		self.assertFalse(isValidStudentID(invalid_id))
		self.assertFalse(isValidStudentID(invalid_id_2))
		print 'studentID_test'
		
	def test_cenario_one(self):
		# saving a new student
		u = User.objects.create_user('assistant4', 'assistant4@assistant.com', 'assistant_password')
		u.first_name = 'Assistant4'
		u.last_name = 'Test'
		u.save()
		
		a = Assistant().create_assistant(u, 'assistant4')
		a.save()

		user = User.objects.create_user('student_test2', 'student_test2@test.com', generate_aleatory_password())
		user.first_name = 'Student2'
		user.last_name = 'Test'
		user.save()
		
		st = Student().create_student(user, 'student_test2', 10000005)
		st.assistant = Assistant.objects.get(username='assistant4')
		st.save()
		
		# verifyng student data
		self.assertEquals(st.number_submissions, 0)
		self.assertEquals(st.solved_exercises, 0)
		self.assertEquals(st.unsolved_exercises, 0)
		self.assertEquals(st.pending_exercises, 0)
		self.assertEquals(st.mean, 0)
		self.assertEquals(st.undelivered_exercises, 0)
		self.assertEquals(st.submission_by_exercise, 0)
		
		# saving two new exercises
		superuser = User.objects.create(username='superuser', password='superuser', email='superuser@test.com')
		superuser.is_superuser = True
		superuser.save()
		ex1 = Exercise().create_exercise('Exercise1_cenario1', 'Description', superuser, True)
		ex1.save()
		ex2 = Exercise().create_exercise('Exercise2_cenario1', 'Description', superuser, True)
		ex2.save()
		
		# verifyng student data
		student = Student.objects.get(pk=st.id)
		self.assertEquals(student.number_submissions, 0)
		self.assertEquals(student.solved_exercises, 0)
		self.assertEquals(student.unsolved_exercises, 0)
		self.assertEquals(student.pending_exercises, 2)
		
		
		self.assertEquals(student.mean, 0)
		self.assertEquals(student.undelivered_exercises, 0)
		self.assertEquals(student.submission_by_exercise, 0)
		
		# saving the tests of exercises
		test1 = Test().create_test('TestExercise1', superuser, ex1)
		test1.save()
		
		test2 = Test().create_test('TestExercise2', superuser, ex2)
		test2.save()
		
		# simulating a submission of student_test2 to exercise ex1
		# first submission
		filename = 'C:\\Documents and Settings\\mariana\Desktop\\TDD\\outrasoma.py'
		submission = Submission().create_submission(st, filename, ex1, 100)
		submission.save()
		#second submission
		filename = 'C:\\Documents and Settings\\mariana\Desktop\\TDD\\outrasoma.py'
		submission = Submission().create_submission(st, filename, ex1, 100)
		submission.save()
		
		# verifyng student data
		self.assertEquals(st.number_submissions, 2)
		self.assertEquals(st.solved_exercises, 0)
		self.assertEquals(st.unsolved_exercises, 0)
		self.assertEquals(st.pending_exercises, 2)
		self.assertEquals(st.mean, 0)
		self.assertEquals(st.undelivered_exercises, 0)
		self.assertEquals(st.submission_by_exercise, 1)
		
		# simulating a submission of student_test2 to exercise ex2
		# first submission
		filename = 'C:\\Documents and Settings\\mariana\Desktop\\TDD\\outrasoma.py'
		submission = Submission().create_submission(st, filename, ex2, 100)
		submission.save()
		#second submission
		filename = 'C:\\Documents and Settings\\mariana\Desktop\\TDD\\outrasoma.py'
		submission = Submission().create_submission(st, filename, ex2, 100)
		submission.save()
		#thrird submission
		filename = 'C:\\Documents and Settings\\mariana\Desktop\\TDD\\outrasoma.py'
		submission = Submission().create_submission(st, filename, ex2, 100)
		submission.save()
		#fourth submission
		filename = 'C:\\Documents and Settings\\mariana\Desktop\\TDD\\outrasoma.py'
		submission = Submission().create_submission(st, filename, ex2, 100)
		submission.save()
		
		# verifyng student data
		self.assertEquals(st.number_submissions, 6)
		self.assertEquals(st.solved_exercises, 0)
		self.assertEquals(st.unsolved_exercises, 0)
		self.assertEquals(st.pending_exercises, 2)
		self.assertEquals(st.mean, 0)
		self.assertEquals(st.undelivered_exercises, 0)
		self.assertEquals(st.submission_by_exercise, 3)
		
		
		
		
# --------------------------- TESTS FOR VIEWS --------------------------- #

	def test_login(self):
		response = self.client.get("/hoopaloo/login/")
		self.assertEquals(response.status_code, 200)
		response = self.client.post("/hoopaloo/login/", {'username':'professor', 'password':'professor'})
		self.assertEquals(response.status_code, 200)
		response = self.client.post("/hoopaloo/login/", {'username':'professor', 'password':'senha'})
		self.assertContains(response, 'Invalid Access', count=None, status_code=200)
		
	def test_register_assistant(self):
		from django.contrib import auth
		user = auth.authenticate(username='professor', password='professor')
		response = self.client.get("/hoopaloo/register_assistant/")
		self.assertEquals(response.status_code, 200)
		
		
		
		

