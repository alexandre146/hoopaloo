# coding: utf-8

#Hoopaloo - Version 1.0 - 2008/2009
#Author: Mariana Romao do Nascimento - mariana@dsc.ufcg.edu.br

from datetime import datetime
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from projectdjango.hoopaloo.models import Student, Exercise, Submission, Result, Test, Assistant, Execution
from projectdjango.hoopaloo.forms import ExerciseForm, LoginForm
import util
from hoopaloo import configuration

# ----------------------------- OPERATIONS WITH EXERCISE (ADD, DELETE, SEE, CHANGE) ---------------------------------------------#

def add_exercise(request):
	"""Register an new exercise."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo.add_exercise"):
			if request.method == 'POST':
				form = ExerciseForm(request.POST) 
				if form.is_valid():
					result = form.save(request.POST, request.user)
					print 'RESULT', result
					if result == True:
						msg = configuration.EXERCISE_ADD_SUCESS
						form = ExerciseForm()
						return render_to_response("add_exercise.html", {'form' : form, 'msg':msg, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
					elif result == None:
						error = configuration.EXERCISE_ADD_ERROR_DATE
						form = ExerciseForm()
						return render_to_response("add_exercise.html", {'form' : form, 'error':error, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
					else:
						error = configuration.EXERCISE_EXISTS
						form = ExerciseForm()
						return render_to_response("add_exercise.html", {'form' : form, 'error':error, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
				else:
					error = configuration.EXERCISE_ADD_ERROR
					return render_to_response("add_exercise.html", {'form' : form, 'error':error, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
			else:
				form = ExerciseForm()
				day = util.get_next_friday(datetime.today())
				friday = str(day.year) + "-" + str(day.month) + "-" + str(day.day) + " " + str(day.hour) + ":" + str(day.minute)
				return render_to_response('add_exercise.html', {'form' : form, 'friday': friday, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
		else:
			error = configuration.EXERCISE_ADD_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))

def exercise(request, exercise_id):
	"""Shows details of exercise with id passed as parameter."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo.see_exercise"):
			if request.method == 'GET':
				exercise = Exercise.objects.get(pk=exercise_id)
				students = Student.objects.all()
				results = Result.objects.all()
				return render_to_response("exercise.html", {'exercise': exercise, 'students' : students, 'results' : results, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
			return render_to_response("error_login.html", {}, context_instance=RequestContext(request))
		else:
			error = configuration.EXERCISE_SEE_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))

def change_exercise(request, exercise_id):
	"""Change details of exercise."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo.change_exercise"):
			e = Exercise.objects.get(pk=exercise_id)
			form = ExerciseForm(request)
			if request.method == 'POST':
				update = form.update(request.POST, e, request.user)
				if update == False:
					error = configuration.EXERCISE_UPDATE_FAIL
					return render_to_response("edit_exercise.html", {'error': error, 'exercise':e, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
				else:
					util.register_action(request.user, configuration.LOG_EDIT_EXERCISE % e.name)
					msg = configuration.EXERCISE_UPDATED_SUCESSFULLY
					return render_to_response("exercise.html", {'msg': msg, 'exercise':e, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
			else:
				return render_to_response("edit_exercise.html", {'exercise': e, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
		else:
			error = confguration.EXERCISE_UPDATE_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:	
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
				
def exercises(request, id_exercise=None):
	"""Show all exercises."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo.change_exercise"):
			exercises = Exercise.objects.all().order_by("date_finish").reverse()
			return render_to_response("exercises.html", {'exercises' : exercises, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
		else:
			error = confguration.EXERCISE_UPDATE_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:	
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
		
def availability_exercise(request, id_exercise):
	"""Redirect to confirmation page before change the availability of an exercise."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo.change_exercise"):
			exercise = Exercise.objects.get(pk=id_exercise)
			return render_to_response("change_availability_exercise.html", {'exercise':exercise, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
		else:
			error = confguration.EXERCISE_UPDATE_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:	
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
	
def change_availability_exercise(request, id_exercise):
	"""View called when the action of change availability of an exercise is actioned."""
	
	if request.user.is_authenticated():
		if request.method == 'GET':
			return render_to_response("change_availability_exercise.html", {'method':request.method,},  context_instance=RequestContext(request))
		else:
			result = util.update_availability(id_exercise)
			if result:
				msg = configuration.EXERCISE_UPDATE_AVAILABILITY
				return render_to_response("change_availability_exercise.html", {'method':request.method, 'msg':msg}, context_instance=RequestContext(request))
			else:
				error = configuration.EXERCISE_UPDATE_AVAILABILITY_ERROR
				return render_to_response("change_availability_exercise.html", {'method':request.method, 'error':error}, context_instance=RequestContext(request))
	else:	
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
		
def delete_exercises(request, exercise_id):
	"""View called when the action of delete an exercise is actioned."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo.delete_exercise"):
			exercise = Exercise.objects.get(pk=exercise_id)
			return render_to_response("delete_exercise.html", {'exercise':exercise, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
		else:
			error = confguration.DELETE_USERS_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:	
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
		
def delete_exercise(request, exercise_id):
	"""Redirect to page with the confimrtaion before change teh availability of an exercise."""
	
	if request.user.is_authenticated():
		if request.method == 'GET':
			return render_to_response("delete_exercise.html", {'method':request.method,},  context_instance=RequestContext(request))
		else:
			exercise = Exercise.objects.get(pk=exercise_id)
			exercise.delete()
			msg = configuration.EXERCISE_DELETED
			util.register_action(request.user, configuration.LOG_DELETE_EXERCISE % exercise.name) 
			return render_to_response("delete_exercise.html", {'method':request.method, 'msg':msg}, context_instance=RequestContext(request))
	else:	
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))	
