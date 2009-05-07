# coding: utf-8

#Hoopaloo - Version 1.0 - 2008/2009
#Author: Mariana Romao do Nascimento - mariana@dsc.ufcg.edu.br

from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from hoopaloo_test.models import Student, Exercise, Submission, Test, Assistant, Actions_log, Execution, Class
from hoopaloo_test.forms import LoginForm
import util
import queries
import configuration
import os
	
		
# ----------------------------------------- VIEWS OF STUDENTS, ASSISTANTS AND TEACHER --------------------------------------- #
def script(request):
	path = "/home/mariana/www/prova1/"
	questao1 = "ProvaQuestao1"
	questao2 = "ProvaQuestao2"
	questao3 = "ProvaQuestao3"
	questao4 = "ProvaQuestao4"
	count_id = 00000001
	for root, dirs, files in os.walk(path, topdown=False):
	    if (root != path) and (files):
	        student_name = root.split("/")[-1]
	        email = student_name + '@hoopaloo_test.com'
	        studentID = count_id + 10
	        count_id = studentID
	        pwd = student_name
	        u = User.objects.create_user(student_name, email, pwd)
	        u.first_name = student_name
	        u.is_active = True
	        u.issuperuser = False
	        u.is_staff = False
	        u.user_permissions.add(37, 54, 55)
	        u.save()
	        st = Student().create_student(u, student_name, str(studentID), 'TurmaProva')
	        st.save()
	        
	        q1 = Exercise.objects.get(name=questao1)
	        q2 = Exercise.objects.get(name=questao2)
	        q3 = Exercise.objects.get(name=questao3)
	        q4 = Exercise.objects.get(name=questao4)
	        
	        if not os.path.exists(settings.MEDIA_ROOT + '/' + student_name + '/' + questao1):
	        	os.makedirs(settings.MEDIA_ROOT + '/' + student_name + '/' + questao1)
			if not os.path.exists(settings.MEDIA_ROOT + '/' + student_name + '/' + questao2):
				os.makedirs(settings.MEDIA_ROOT + '/' + student_name + '/' + questao2)
			if not os.path.exists(settings.MEDIA_ROOT + '/' + student_name + '/' + questao3):
				os.makedirs(settings.MEDIA_ROOT + '/' + student_name + '/' + questao3)
			if not os.path.exists(settings.MEDIA_ROOT + '/' + student_name + '/' + questao4):
				os.makedirs(settings.MEDIA_ROOT + '/' + student_name + '/' + questao4)
				
				
	        filename1 = settings.MEDIA_ROOT + '/' + student_name + '/' + questao1 + '/' + questao1 + '.py'
	        filename2 = settings.MEDIA_ROOT + '/' + student_name + '/' + questao2 + '/' + questao2 + '.py'
	        filename3 = settings.MEDIA_ROOT + '/' + student_name + '/' + questao3 + '/' + questao3 + '.py'
	        filename4 = settings.MEDIA_ROOT + '/' + student_name + '/' + questao4 + '/' + questao4 + '.py'
	        
	        for f in files:
	            st_file = open(root + '/' + f, 'r')
	            contend = st_file.read()
	            size = os.path.getsize(root + '/' + f)
	            if f == 'q1.py': 
	                other_file = open(filename1, 'wb')
	                submission = Submission().create_submission(st, filename1, q1, size)
	            elif f == 'q2.py':
	                other_file = open(filename2, 'wb')
	                submission = Submission().create_submission(st, filename2, q2, size)
	            elif f == 'q3.py':
	                other_file = open(filename3, 'wb')
	                submission = Submission().create_submission(st, filename3, q3, size)
	            else:   
	                other_file = open(filename4, 'wb')
	                submission = Submission().create_submission(st, filename4, q4, size)
	                
	            other_file.write(contend)
	            st_file.close()
	            other_file.close()
	            
	            submission.save()
	        
	            st.number_submissions += 1
	            st.save()
        return render_to_response("teacher_view.html", {}, context_instance=RequestContext(request))
       
       
def teacher_view(request):
	"""Redirect to initial page of teacher."""
	
	if request.user.is_authenticated():
		if request.user.is_superuser:
			if request.method == 'GET':
				classes = queries.get_classes(request.user)
				s = []
				for c in classes:
					students = queries.get_ordered_class_student(c.id)
					for st in students:
						s.append(st)
				num_exercises = queries.get_number_exercises()
				return render_to_response("teacher_view.html", {'students':s, 'num_exercises':num_exercises,}, context_instance=RequestContext(request))
		else:
			error = configuration.TEACHER_VIEW_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
		
def exercise_percentual(request, exercise_id):
	"""Shows the percentuals of students that passed in X% of tests."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo_test.see_exercise"):
			if request.method == 'GET':
				exercise = queries.get_exercise(exercise_id)
				students = queries.get_all_students()
				percentual = configuration.PERCENT_OF_TESTS
				st_percent = util.calculate_percentual(percentual, exercise.number_tests, students, exercise)
				return render_to_response("exercise_percentual.html", {'st_percent':st_percent, 'is_assistant': util.is_assistant(request.user), 'exercise': exercise, }, context_instance=RequestContext(request))
		else:
			error = configuration.EXERCISE_SEE_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
		
def assistant_view(request):
	"""Redirect to a page with the students assigned to this assistant."""
	
	if request.user.is_authenticated():
		profile = request.user.get_profile()
		if isinstance(profile, Assistant):
			if request.method == 'GET':
				students = queries.get_ordered_assistant_students()
				user = request.user
				return render_to_response("assistant_view.html", {'students':students, 'user':user,}, context_instance=RequestContext(request))
		else:
			error = configuration.ASSISTANT_VIEW_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
		

def score_percentual(request, exercise_id):
	"""Shows the percentuals of students that receive the score between X and Y."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo_test.see_exercise"):
			if request.method == 'GET':
				exercise = queries.get_exercise(exercise_id)
				results = queries.get_all_last_submissions(exercise.id)
				score_percentual = configuration.PERCENT_OF_SCORE
				score_percent = util.calculate_score_percentual(score_percentual, results, exercise)
				return render_to_response("note_percentual.html", {'note_percent':score_percent, 'exercise':exercise, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
		else:
			error = configuration.EXERCISE_SEE_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
		
def student_exercises(request, student_id):
	"""Shows all exercises of studen represented by student_id."""
	
	if request.user.is_authenticated():
		if request.user.has_perm(".see_results"):
			if request.method == 'GET':
				student = queries.get_student(student_id)
				informations = util.student_exercises(student_id)
				return render_to_response("exercises_student.html", {'informations':informations, 'student':student, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
		else:
			error = configuration.RESULT_SEE_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
		
def delivered_exercises_student(request, student_id):
	""""Shows to student a list with the exercises that he/she delivered."""
	
	if request.user.is_authenticated():
		if request.method == 'GET':
			delivered = util.get_delivered_exercises(student_id)
			student = queries.get_student(student_id)
			explication = configuration.DELIVERED_EXERCISES_MSG
			return render_to_response("delivered_exercises_student.html", {'delivered' : delivered, 'explication': explication, 'student':student, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
		
def list_percentual(request, percent, id_exercise):
	"""Shows a list of students that aimed a percentual X of pass in the tests."""
	
	if request.user.is_authenticated():
		students = util.get_students_percent(percent, id_exercise)
		return render_to_response("list_percentual.html", {'students' : students, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
	else:	
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
		
def list_score_percentual(request, index, id_exercise):
	"""Shows a list of students that aimed a percentual of score between X and Y."""
	
	if request.user.is_authenticated():
		students = util.get_students_score_percent(int(index), id_exercise)
		return render_to_response("list_note_percentual.html", {'students' : students, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
	else:	
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))						
def all_students(request):
	"""List all students."""
	
	if request.user.is_authenticated():
		if request.user.is_superuser:
			if request.method == 'GET':
				students = queries.get_all_students_ordered()
				return render_to_response("teacher_view.html", {'students':students,}, context_instance=RequestContext(request))
		else:
			error = configuration.TEACHER_VIEW_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))

def global_assistant_view(request):
	"""Redirect to a page with all students."""
	
	if request.user.is_authenticated():
		if isinstance(request.user.get_profile(), Assistant):
			if request.method == 'GET':
				students = queries.get_all_students_ordered()
				user = request.user
				return render_to_response("assistant_view.html", {'students':students, 'user':user,}, context_instance=RequestContext(request))
		else:
			error = configuration.ASSISTANT_VIEW_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))

def available_exercises(request):
	"""Shows all available exercises."""
	
	if request.user.is_authenticated():
		if request.method == 'GET':
			available = queries.get_ordered_available_exercises()
			student = request.user.get_profile()
			explication = configuration.AVAILABLE_EXERCISES_MSG
			return render_to_response("student_view.html", {'undelivered' : available, 'explication' : explication, 'student':student, }, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
			
def delivered_exercises(request):
	"""Shows all delivered exercises."""
	
	if request.user.is_authenticated():
		if request.method == 'GET':
			student = request.user.get_profile()
			delivered = util.get_delivered_exercises(student.id)
			explication = configuration.DELIVERED_EXERCISES_MSG
			return render_to_response("student_view.html", {'delivered' : delivered, 'explication': explication, 'student':student, }, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))

def undelivered_exercises(request):
	"""Shows all undelivered exercises."""
	
	if request.user.is_authenticated():
		if request.method == 'GET':
			exercises = queries.get_ordered_unavailable_exercises()
			student = request.user.get_profile()
			undelivered = []
			for ex in exercises:
				submissions = queries.get_number_student_submissions(ex.id, student.id)
				if submissions == 0:
					undelivered.append(ex)
			explication = configuration.UNDELIVERED_EXERCISES_MSG
			return render_to_response("student_view.html", {'undelivered' : undelivered, 'explication':explication, 'student':student, }, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
	
# ------------------------------------ ACTIONS OF USERS ------------------------------------- #
def actions(request):
	"""Shows all actions realized in the system."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo_test.see_actions"):
			# last 100 actions
			actions = queries.get_last_100_actions()
			return render_to_response("actions.html", {'actions':actions, }, context_instance=RequestContext(request))
		else:
			error = configuration.SEE_ACTIONS_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:	
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
