# coding: utf-8
import os
from datetime import datetime, date, timedelta
from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from hoopaloo_test import forms
from hoopaloo_test.models import Exercise, Student, Assistant, Submission, Exercise, Execution, Test, Class
from hoopaloo_test.util import *
import queries

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
		self.aux_create_assistant()
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
		
	def aux_do_submission(self, student, exercise_name):
		self.aux_create_submission(exercise_name)
		student.number_submissions += 1
		student.submission_by_exercise = student.number_submissions/len(Exercise.objects.all())
		student.save()
		
	def Oktest_create_exercise(self):
		self.aux_create_exercise(5)
		
		exercise = Exercise.objects.get(name='Ex_test5')
		self.assertEquals(exercise.name, 'Ex_test5')
		self.assertEquals(exercise.description, 'Description Test')
		self.assertTrue(exercise.available)
		
	def test_register_assistant(self):
		self.aux_create_assistant()
		
		assistant = Assistant.objects.get(username='assistant')
		self.assertEquals(assistant.username, 'assistant')
		self.assertEquals(assistant.user.email, 'assistant@assistant.com')
		self.assertEquals(assistant.user.first_name, 'Assistant')
		self.assertEquals(assistant.user.last_name, 'Test')

	def test_register_student(self):
		self.aux_create_student()
		
		student = Student.objects.get(pk=1)
		self.assertEquals(student.username, 'student_test')
		self.assertEquals(student.user.email, 'student_test@test.com')
		self.assertEquals(int(student.studentID), 10000001)
		self.assertEquals(student.user.first_name, 'Student')
		self.assertEquals(student.user.last_name, 'Test')
				
	def test_create_submission(self):
		
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
		
	def test_username(self):
		user = User.objects.create_user('student_test5', 'student_test5@test.com', generate_aleatory_password())
		user.save()

		self.assertFalse(isValidUsername('student_test5'))
		self.assertTrue(isValidUsername('mariana'))
		
	def test_email(self):
		valid_email = 'mari.ufcg@gmail.com'
		invalid_email = 'mari.com'
		
		self.assertTrue(isValidEmail(valid_email))
		self.assertFalse(isValidEmail(invalid_email))
		
	def test_studentID(self):
		valid_id = 12345678
		invalid_id = 123
		invalid_id_2 = "invalid"
		
		self.assertTrue(isValidStudentID(valid_id))
		self.assertFalse(isValidStudentID(invalid_id))
		self.assertFalse(isValidStudentID(invalid_id_2))
		
	def test_cenario_one(self):
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
		self.aux_do_submission(st, "Ex_test1")
		#second submission
		self.aux_do_submission(st, "Ex_test1")

		# simulating a submission of student_test2 to exercise ex2
		# first submission
		self.aux_do_submission(st, "Ex_test2")
		#second submission
		self.aux_do_submission(st, "Ex_test2")
		#thrird submission
		self.aux_do_submission(st, "Ex_test2")
		#fourth submission
		self.aux_do_submission(st, "Ex_test2")
					
		student = Student.objects.get(pk=st.id)
		# verifyng student data
		self.assertEquals(student.number_submissions, 6)
		self.assertEquals(student.submission_by_exercise, 3.0)
		
	def test_pre_and_post_save_exercise(self):
		self.aux_create_student()
		st1 = Student.objects.get(username="student_test")
		
		self.assertEquals(0, st1.pending_exercises)
		self.aux_create_exercise(1)
		
		st2 = Student.objects.get(username="student_test")
		self.assertEquals(1, st2.pending_exercises)
		self.failureException(Test.objects.get(name='Test_Ex_test1'))
		self.assertTrue(os.path.exists(settings.MEDIA_ROOT + '/tests/Test_Ex_test1.py'))
		
# TESTING QUERIES
	
	def test_submissions_queries(self):
		self.aux_create_student()		
		st = Student.objects.get(username="student_test")
		self.aux_create_exercise(1)
		self.aux_create_exercise(2)
		
		ex1 = Exercise.objects.get(name='Ex_test1')
		ex2 = Exercise.objects.get(name='Ex_test2')
		
		self.aux_do_submission(st, "Ex_test1")
		sub1 = Submission.objects.filter(id_exercise=ex1).order_by('date')[0]
		
		self.aux_do_submission(st, "Ex_test2")
		sub2 = Submission.objects.filter(id_exercise=ex2).order_by('date')[0]
		
		self.aux_do_submission(st, "Ex_test1")
		sub3 = Submission.objects.filter(id_exercise=ex1).order_by('date')[1]
		
		self.aux_do_submission(st, "Ex_test2")
		sub4 = Submission.objects.filter(id_exercise=ex2).order_by('date')[1]
		
		self.aux_do_submission(st, "Ex_test2")
		sub5 = Submission.objects.filter(id_exercise=ex2).order_by('date')[2]
		
		# get_submissions(exercise_id, student_id)
		submissions = queries.get_submissions(ex1.id, st.id)
		self.assertEquals(2, len(submissions))
		
		# get_ordered_submissions(exercise_id, student_id)
		submissions_ordered = queries.get_ordered_submissions(ex1.id, st.id)
		self.assertEquals(2, len(submissions_ordered))
		d1 = submissions_ordered[0]
		d2 = submissions_ordered[1]
		self.assertTrue(d2 < d1)
		
		# get_student_submissions(student_id)
		
		# get_submission(submission_id)
		
		# get_ordered_student_submissions(student_id)
		all_ordered_student_submissions = queries.get_ordered_student_submissions(st.id)
		self.assertEquals(5, len(all_ordered_student_submissions))
			
		# get_number_student_submissions(exercise_id, student_id)
		
		# get_last_submission(exercise_id, student_id)
		last_submission1 = queries.get_last_submission(ex1.id, st.id)
		last_submission2 = queries.get_last_submission(ex2.id, st.id)
		self.assertEquals(all_ordered_student_submissions[1].id, last_submission1.id)
		self.assertEquals(all_ordered_student_submissions[0].id, last_submission2.id)
		
		# get_exercise_submissions(exercise_id)
		exercise_submissions1 = queries.get_exercise_submissions(ex1.id)
		self.assertEquals(2, len(exercise_submissions1))
		self.assertEquals(all_ordered_student_submissions[2].id, exercise_submissions1[0].id)
		self.assertEquals(all_ordered_student_submissions[3].id, exercise_submissions1[1].id)
		
		exercise_submissions2 = queries.get_exercise_submissions(ex2.id)
		self.assertEquals(3, len(exercise_submissions2))
		
		self.assertEquals(all_ordered_student_submissions[2].id, exercise_submissions2[0].id)
		self.assertEquals(all_ordered_student_submissions[1].id, exercise_submissions2[2].id)
		self.assertEquals(all_ordered_student_submissions[0].id, exercise_submissions2[1].id)
		
		# get_number_total_student_submissions(student_id)
		number = queries.get_number_total_student_submissions(st.id)
		self.assertEquals(5, number)
		
		# get_all_submissions()
		all_submissions = queries.get_all_submissions()
		self.assertEquals(5, len(all_submissions))
		self.assertEquals("Ex_test1", all_submissions[0].id_exercise.name)
		self.assertEquals("Ex_test2", all_submissions[1].id_exercise.name)
		self.assertEquals("Ex_test1", all_submissions[2].id_exercise.name)
		self.assertEquals("Ex_test2", all_submissions[3].id_exercise.name)
		self.assertEquals("Ex_test2", all_submissions[4].id_exercise.name)
		
		# get_all_last_submissions(exercise_id)
		last_submissions = queries.get_all_last_submissions(ex1.id)
		self.assertEquals(1, len(last_submissions))		
		self.assertEquals(all_ordered_student_submissions[1].id, last_submissions[0].id)
		
	def test_exercise_queries(self):
		
		# get_all_exercises():
		self.aux_create_exercise(1)
		self.aux_create_exercise(2)
		
		exercises = queries.get_all_exercises()
		self.assertEquals(2, len(exercises))
		self.assertEquals("Ex_test1", exercises[0].name)
		self.assertEquals("Ex_test2", exercises[1].name)
		
		# get_number_exercises():
		self.assertEquals(2, queries.get_number_exercises())
		
		# get_exercise()
		self.assertEquals("Ex_test1", queries.get_exercise(1).name)
		
		# get_all_exercises_ordered()
		self.assertEquals(1, queries.get_all_exercises_ordered()[0].id)
		self.assertEquals(2, queries.get_all_exercises_ordered()[1].id)
		
		# get_available_exercises()
		ex2 = Exercise.objects.get(name='Ex_test2')
		ex2.available = False
		ex2.save()
		self.assertEquals(1, queries.get_available_exercises()[0].id)
		self.assertEquals("Ex_test1", queries.get_available_exercises()[0].name)
		
		# get_unavailable_exercises
		self.assertEquals(1, len(queries.get_unavailable_exercises()))
		
		# get_ordered_unavailable_exercises()
		ex1 = Exercise.objects.get(name='Ex_test1')
		ex1.available = False
		ex1.save()
		self.assertEquals(1, queries.get_ordered_unavailable_exercises()[0].id)
		self.assertEquals(2, queries.get_ordered_unavailable_exercises()[1].id)
		
		# get_ordered_available_exercises()
		ex1.available = True
		ex1.save()
		ex2.available = True
		ex2.save()
		self.assertEquals(1, queries.get_ordered_available_exercises()[0].id)
		self.assertEquals(2, queries.get_ordered_available_exercises()[1].id)
	
		# get_reverse_ordered_available_exercises()
		self.assertEquals(2, queries.get_ordered_available_exercises()[1].id)
		self.assertEquals(1, queries.get_ordered_available_exercises()[0].id)
		
		# get_available_exercises_ordered_by_name()
		self.assertEquals("Ex_test1", queries.get_available_exercises_ordered_by_name()[0].name)
		self.assertEquals("Ex_test2", queries.get_available_exercises_ordered_by_name()[1].name)
		
		# get_number_available_exercises()
		self.assertEquals(2, queries.get_number_available_exercises())
		
		ex1.available = False
		ex1.save()
		self.assertEquals(1, queries.get_number_available_exercises())
		
		# get_number_unavailable_exercises()
		self.assertEquals(1, queries.get_number_unavailable_exercises())
		
		ex2.available = False
		ex2.save()
		
		self.assertEquals(2, queries.get_number_unavailable_exercises())
		
		# get_exercise_from_name
		self.assertEquals(1, queries.get_exercise_from_name("Ex_test1").id)
		self.assertEquals(2, queries.get_exercise_from_name("Ex_test2").id)
		
		# get_solved_exercises()
		self.aux_create_student()
		st = Student.objects.get(username="student_test")
		self.aux_do_submission(st, "Ex_test1")
		
		# get_solved_exercises(student_id)
		self.aux_do_submission(st, "Ex_test1")
		sub1 = Submission.objects.filter(id_exercise=ex1).order_by('date')[0]
		self.aux_do_submission(st, "Ex_test2")
		sub2 = Submission.objects.filter(id_exercise=ex2).order_by('date')[0]
		
		sub1.veredict = "Pass"
		sub1.save()
		sub2.veredict = "Fail"
		sub2.save()
		
		self.assertEquals(1, queries.get_solved_exercises(st.id)[0].id)
		
		# get_number_solved_exercises(student_id)
		self.assertEquals(1, queries.get_number_solved_exercises(st.id))
		
		# get_unsolved_exercises(student_id)
		self.assertEquals(1, queries.get_unsolved_exercises(st.id)[0].id)
		
		# get_number_unsolved_exercises()
		self.assertEquals(1, queries.get_number_unsolved_exercises(st.id))
		
		# get_undelivered_exercises(student_id)
		self.aux_create_exercise(3)
		ex3 = Exercise.objects.get(name='Ex_test3')
		ex3.available = False
		ex3.save()
		
		self.assertEquals(3, queries.get_undelivered_exercises(st.id)[0].id)
		self.assertEquals(1, queries.get_number_undelivered_exercises(st.id))
		
		st.delete()
		sub1.delete()
		sub2.delete()
		sub3.delete()
		ex3.delete()
		ex2.delete()
		ex1.delete()
		
# TESTING UTIL FUNCTIONS 

	def test_generate_aleatory_password(self):
		password1 = generate_aleatory_password()
		password2 = generate_aleatory_password()
		self.assertEquals(6, len(password1))
		self.assertEquals(6, len(password2))
		self.assertNotEquals(password1, password2)

	def test_listToString(self):
		my_list1 = [" ", " ", " "]
		self.assertEquals(" \n \n \n", listToString (my_list1))
		
		my_list2 = [1, "Nothing"]
		self.assertEquals("1\nNothing\n", listToString (my_list2))
		
		my_list3 = []
		self.assertEquals("", listToString(my_list3))
		
		my_list4 = ["All"]
		self.assertEquals("All\n", listToString(my_list4))
		
		my_list5 = [None]
		self.assertEquals("", listToString(my_list5))
		
		my_list6 = None
		self.assertEquals("", listToString(my_list6))
		
	def test_isValidUsername(self):
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
		
	def test_isValidEmail(self):
		self.assertTrue(isValidEmail("mariana@dsc.ufcg.edu.br"))
		self.assertFalse(isValidEmail(""))
		self.assertFalse(isValidEmail(None))	
		self.assertFalse(isValidEmail("&¨%$$#@"))
		self.assertFalse(isValidEmail(" "))
		self.assertFalse(isValidEmail("mariana.dsc.ufcg.edu.br"))
		self.assertFalse(isValidEmail("mariana@"))
		
	def test_isValidStudentID(self):
		self.assertTrue(isValidStudentID("12345678"))
		self.assertFalse(isValidStudentID("mnfbnmbfn"))
		self.assertFalse(isValidStudentID(" "))
		self.assertFalse(isValidStudentID(""))
		self.assertFalse(isValidStudentID(None))
		
	def test_get_next_friday(self):
		td = date.today()
		friday = td + timedelta(2)
		self.assertEquals(friday, get_next_friday(td))	
		
		day1 = date(2009, 05, 18)
		day2 = date(2009, 05, 22)
		self.assertEquals(day2, get_next_friday(day1))
		
		day3 = date(2009, 02, 28)
		day4 = date(2009, 03, 06)
		self.assertEquals(day4, get_next_friday(day3))
		
	
# --------------------------- TESTS FOR VIEWS --------------------------- #

	def test_login(self):
		response = self.client.get("/hoopaloo_test/login/")
		self.assertEquals(response.status_code, 200)
		response = self.client.post("/hoopaloo_test/login/", {'username':'professor', 'password':'professor'})
		self.assertEquals(response.status_code, 200)
		response = self.client.post("/hoopaloo_test/login/", {'username':'professor', 'password':'senha'})
		self.assertContains(response, 'Invalid Access', count=None, status_code=200)
		
	def test_register_assistant(self):
		from django.contrib import auth
		user = auth.authenticate(username='professor', password='professor')
		response = self.client.get("/hoopaloo_test/register_assistant/")
		self.assertEquals(response.status_code, 200)
		
