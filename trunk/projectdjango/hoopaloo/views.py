# coding: utf-8

#Hoopaloo - Version 1.0 - 2008/2009
#Author: Mariana Romao do Nascimento - mariana@dsc.ufcg.edu.br

from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from projectdjango.hoopaloo.models import Student, Exercise, Submission, Result, Test, Assistant, Actions_log, Execution, Class
from projectdjango.hoopaloo.forms import LoginForm
import util
from hoopaloo import configuration
	
		
# ----------------------------------------- VIEWS OF STUDENTS, ASSISTANTS AND TEACHER --------------------------------------- #
def teacher_view(request):
	"""Redirect to initial page of teacher."""
	
	if request.user.is_authenticated():
		if request.user.is_superuser:
			if request.method == 'GET':
				classes = Class.objects.filter(teacher=request.user.id)
				s = []
				for c in classes:
					students = Student.objects.filter(student_class=c.id).order_by('username')
					for st in students:
						s.append(st)
				
				num_exercises = len(Exercise.objects.all())
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
		if request.user.has_perm("hoopaloo.see_exercise"):
			if request.method == 'GET':
				exercise = Exercise.objects.get(pk=exercise_id)
				students = Student.objects.all()
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
				students = Student.objects.filter(assistant=profile.id).order_by('username')
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
		if request.user.has_perm("hoopaloo.see_exercise"):
			if request.method == 'GET':
				exercise = Exercise.objects.get(pk=exercise_id)
				results = Result.objects.all()
				note_percentual = configuration.PERCENT_OF_NOTE
				note_percent = util.calculate_note_percentual(note_percentual, results, exercise)
				return render_to_response("note_percentual.html", {'note_percent':note_percent, 'exercise':exercise, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
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
				student = Student.objects.get(pk=student_id)
				results = Result.objects.filter(id_student=student_id).order_by('id_exercise').reverse()
				informations = []
				for r in results:
					ex = Exercise.objects.get(pk=r.id_exercise.id)
					submited = Submission.objects.filter(id_student=student_id, id_exercise=ex.id)
					if r.veredict == 'Pass':
						solved = True
					else:
						solved = False
					date = submited.order_by("date")[len(submited)-1].date
					percentage = util.calculate_correct_percentage(ex)
					d = util.Table_Delivered(ex, r.num_submissions, date, ex.number_tests, solved, r.errors_number, r.note, percentage)
					informations.append(d)
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
			student = Student.objects.get(pk=student_id)
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
				students = Student.objects.all().order_by('username')
				num_exercises = len(Exercise.objects.all())
				return render_to_response("teacher_view.html", {'students':students, 'num_exercises':num_exercises,}, context_instance=RequestContext(request))
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
				students = Student.objects.all().order_by('username')
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
			available = Exercise.objects.filter(available=True).order_by('date_finish')
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
			exercises = Exercise.objects.filter(available=False).order_by('date_finish')
			student = request.user.get_profile()
			undelivered = []
			for ex in exercises:
				try:
					submissions = Submission.objects.get(id_student=student.id, id_exercise=ex.id)
				except:
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
		if request.user.has_perm("hoopaloo.see_actions"):
			# last 100 actions
			actions = Actions_log.objects.all().order_by('date').reverse()[:100]
			return render_to_response("actions.html", {'actions':actions, }, context_instance=RequestContext(request))
		else:
			error = configuration.SEE_ACTIONS_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:	
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
