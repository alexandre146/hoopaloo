# coding: utf-8

#Hoopaloo - Version 1.0 - 2008/2009
#Author: Mariana Romao do Nascimento - mariana@dsc.ufcg.edu.br

import smtplib
import util
import random
import sha
import os
import re
from datetime import date, datetime
from django.utils.encoding import smart_str
from django.core.files.uploadedfile import UploadedFile
from django.core.files.storage import default_storage
from django.contrib.auth.models import get_hexdigest
from django.core.files.base import ContentFile
from django.forms.util import ValidationError
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import encoding
from django.conf import settings
from django import forms
import configuration
from hoopaloo_test.models import Exercise, Student, Assistant, Test, Submission, Class
from hoopaloo_test.util import update_students, isValidStudentID, generate_aleatory_password, isValidEmail, isValidUsername, listToString, send_email, register_action, get_time_unavailability, Change_Availability
import queries

class ExerciseForm(forms.Form):
	"""This form represents the registration of new exercise.
	The fields are name, description, if it is available and owner.
	Addionally the teacher/assistant can add a test for this exercise.
	"""
	
	# Fields of exercise
	name = forms.CharField(max_length=50)
	description = forms.Field(widget=forms.Textarea, required=False) 
	available = forms.BooleanField(initial=True, required=False)
	date_finish = forms.DateTimeField(required=False)
	
	def save(self, new_data, user):
		"""Save the new exercise and the associated tests"""
		
		name_ex = new_data['name']
		description = new_data['description']
		if 'available' in new_data:
			available = new_data['available']
		else:
			available = False
		owner_id = user
		
		try:
			ex_date = util.create_datetime(new_data['calendar'])
		except:
			ex_date = None
		
		try:
			e = queries.get_exercise_from_name(name_ex)
			return False
		except:
			pass
			
			new_exercise = Exercise().create_exercise(name_ex, description, owner_id, available, ex_date)
			if new_exercise:
				new_exercise.save()
			else:
				return None
		register_action(user, configuration.LOG_ADD_EXERCISE % name_ex)
		return True
				
	def update(self, new_data, exercise, user):
		
		name_ex = new_data['name']
		description = new_data['description']
		if 'available' in new_data:
			available = new_data['available']
			exercise.date_availability = datetime.now()
		else:
			available = False
		
		try:
			ex_date = util.create_datetime(new_data['calendar'])
			exercise.date_finish = ex_date 
		except:
			ex_date = None			
			
		if not exercise.available and available:
			try:
				t = get_time_unavailability(exercise.date_finish, exercise.date_availability)
				cron = Change_Availability(exercise.name, t)
				cron.init_cont()
			except:
				return False
	
		exercise.name = name_ex
		exercise.description = description
		exercise.available = available
		exercise.owner = user
		exercise.save()
		
		return True
		
class SubmissionForm(forms.Form):
	"""This form represents a submission of a student with the related exercise 
	and the file to be uploaded"""
	
	#Fields of submission
	file = forms.FileField()
	exercise = forms.ModelChoiceField(queryset=queries.get_available_exercises_ordered_by_name())
	
	def save(self, request):
		"""Save the new submission"""
		user_st = queries.get_student_from_user_id(request.user)
		ex_id = request.POST['exercise']
		exercise = queries.get_exercise(ex_id)
		
		# verify if exists other submissions of same student for this same exercise
		# if exists then the file must be copied to other folder
		self.verify_previous_submission(user_st, exercise)
		# saving the uploaded file 
		filename = self.handle_uploads(request)
		
		file_size = request.FILES['file'].size
				
		submission = Submission().create_submission(user_st, filename, exercise, file_size)
		submission.save()
		
		number_ex = float(queries.get_number_exercises())
		#doing updtade in student
		student = user_st
		student.number_submissions += 1
		student.submission_by_exercise = student.number_submissions/number_ex
		student.save()
		
		register_action(request.user, configuration.LOG_SUBMISSION % exercise.name)
		return queries.get_last_submission(exercise.id, student.id)
			
	
	def verify_previous_submission(self, student, exercise):
		"""verify if exists other submissions of same student for this same exercise.
		If exists then the file must be copied to other folder."""
		
		
		exercise_dir = '/' + student.username + '/' + exercise.name
		full_path = settings.MEDIA_ROOT + exercise_dir + '/Old_Versions/' 
		
		number = queries.get_number_student_submissions(exercise.id, student.id)
		if number > 0:
			submissions = queries.get_ordered_submissions(exercise.id, student.id)
			sub = submissions[0]
			file = sub.solution_file._name
			old_path = open(file)
			
			if not os.path.exists(full_path):
				os.makedirs(full_path)
			# the file name is something like 'Ex01_1.py' (<exercise name><number of submssions to that exercise><.py>)
			new_path = open(full_path + exercise.name + '_' + str(number) + '.py', 'wb')
			
			# coping the old file
			contend = old_path.read()
			new_path.write(contend)
			
			old_path.close()
			new_path.close()
			
			# removing the old file
			os.remove(file)
			# updating the path to file in the submission object
			sub.solution_file = full_path + exercise.name + '_' + str(number) + '.py'
			sub.save()
	
	def handle_uploads(self, request):
		"""Handle the file uploaded, storaging it in an specific directory."""
		
		if 'file' in request.FILES:
			upload = request.FILES['file']
			id_ex = request.POST['exercise']
			exercise_name = queries.get_exercise(id_ex).name
			
			upload_dir = '/' + request.user.username + '/' + exercise_name + '/'
			upload_full_path = settings.MEDIA_ROOT + upload_dir
		
			if not os.path.exists(upload_full_path):
				os.makedirs(upload_full_path)
			
			st = request.user.get_profile()
			file_path = upload_full_path + '/' + exercise_name + '.py'
			
			dest = open(file_path, 'wb')
			for chunk in upload.chunks():
				dest.write(chunk)
			dest.close()
			return file_path
		
	class Meta:
		model = Submission
		exclude = ('solution_file',)
		
class LoginForm(forms.Form):
	"""Form to login operation"""
	
	username = forms.CharField(max_length=30) 
	password = forms.CharField(max_length=128, widget=forms.PasswordInput) 

class ChangePasswordForm(forms.Form):
	"""Form to change password."""
	
	old_password = forms.CharField(label='Enter the current password', max_length=128, widget=forms.PasswordInput) 
	password1 = forms.CharField(label='Enter the new password', max_length=128, widget=forms.PasswordInput) 
	password2 = forms.CharField(label='Password confirmation', max_length=128, widget=forms.PasswordInput) 

	
class ForgotPasswordForm(forms.Form):
	"""Form for password recuperation"""
	
	email = forms.EmailField()
	
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
		
class AssignStudentsForm(forms.Form):
	"""Form to register assigns between assistants and students."""
	
	assigns = forms.Field(widget=forms.Textarea({'cols': '50', 'rows': '15'}), required=True)
	
	def save(self, new_data):
		assigns = new_data.POST['assigns'].split('\r\n')
		
		for a in assigns:
			line = a.split()
			assistant = line[0]
			students = line[1:]
			str_students = []
			errors = []
			
			for s in students:
				try:
					st = queries.get_student_from_username(s)
					st.assistant = queries.get_assistant_from_username(assistant)
					st.save()
				except:
					errors.append(str(a))
			if not students:
				errors.append(str(a))
			
			for s in students:
				str_students.append(str(s)) 
			register_action(new_data.user, configuration.LOG_ASSIGN_STUDENTS % (assistant, str_students))
		
		result = dict()
		if len(errors) != 0:
			result['assigns'] = listToString(errors)
		return result
				
class RegisterAssistantForm(forms.Form):
	"""Register a new assistant and add him to the system"""

	assistants = forms.Field(widget=forms.Textarea({'cols': '50', 'rows': '15'}), required=True)
	
	# This method receives an object 'request.POST' and gets its informations.
	# Makes the validation of username and passowrd and save the new teacher in database
	def save(self, new_data):
		"""This method receives an object 'request.POST' and gets its informations.
		Makes the validation of username and password and save the new assistant in database."""
		
		assistants = new_data.POST['assistants'].split('\r\n')
		assistants_err = []
		count = 0
		for assistant in assistants:
			if (assistant != '' and assistant != ' '):
				info = assistant.split()
				try:
					username = info[0]
					email = info[1]
					name = ''
					for n in info[2:]:
						name += str(n)+' '
						
					if (isValidUsername(username) and isValidEmail(email)):
		
						pwd = generate_aleatory_password()
						u = User.objects.create_user(username, email, pwd)
						u.first_name = info[2]
						u.last_name = info[len(info)-1]
						u.is_active = True
						u.issuperuser = False
						u.is_staff = True
						for i in range(61):
							u.user_permissions.add(i+1)
						u.save()
						ass = Assistant().create_assistant(u, username)
						ass.save()
						
						register_action(new_data.user, configuration.LOG_ADD_ASSISTANT % ass.username)
						
						msg = configuration.PASSWORD_EMAIL % (smart_str(username), smart_str(pwd))
						subject = "Welcome to Hoopaloo"
						send_email(u.email, subject, msg)
					else:
						assistants_err.append(str(assistant))
					
				except:
					assistants_err.append(str(assistant))
			else:
				count+=1
		if count == len(assistants):
			assistants_err.append(' ')
		result = dict()
		if len(assistants_err) != 0:
			result['assistants'] = listToString(assistants_err)
		return result
			
class RegisterStudentForm(forms.Form):
	"""Register a new student and add him to the system"""
	
	students = forms.Field(widget=forms.Textarea({'cols': '80', 'rows': '20'}), required=True)

	# This method receives an object 'request.POST' and gets its informations.
	# Makes the validation of username and password and save the new student in database
	
	def save(self, new_data):
		"""This method receives an object 'request.POST' and gets its informations.
		Makes the validation of username and password and save the new student in database."""
		students = new_data.POST['students'].split('\r\n')
		students_err = []
		count = 0
		for student in students:
			if (student != '' and student != ' '):
				info = student.split()
				#try:
				matr = info[0]
				username = info[1]
				email = info[2]
				_class = info[3]
				name = ''
				for n in info[4:]:
					name += str(n)+' '
				if (isValidUsername(username) and isValidEmail(email) and isValidStudentID(matr)):
					pwd = generate_aleatory_password()
					u = User.objects.create_user(username, email, pwd)
					u.first_name = info[4]
					if (u.first_name != info[len(info)-1]):
						u.last_name = info[len(info)-1]
					u.is_active = True
					u.issuperuser = False
					u.is_staff = False
					u.user_permissions.add(37, 54, 55)
					u.save()
					st = Student().create_student(u, username, int(matr), str(_class))
					st.save()
					
					util.copy_test_files(st)
					register_action(new_data.user, configuration.LOG_ADD_STUDENT % st.username)
				
					msg = configuration.PASSWORD_EMAIL % (smart_str(username), smart_str(pwd))
					subject = "Welcome to Hoopaloo"
					
					send_email(u.email, subject, msg)
				
				else:
					students_err.append(str(student))
				#except:
						#students_err.append(str(student))
			else:
				count+=1
		if count == len(students):
			students_err.append(' ')
		result = dict()
		if len(students_err) != 0:
			result['students'] = listToString(students_err)
		return result