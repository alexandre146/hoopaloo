# coding: utf-8

#Hoopaloo - Version 1.0 - 2008/2009
#Author: Mariana Romao do Nascimento - mariana@dsc.ufcg.edu.br

import os
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from hoopaloo.models import Student, Exercise, Test, UnderTest
from hoopaloo.forms import ChoiceSubmissionsForm, LoginForm
import util
import queries
import configuration


# ----------------------------------- OPERATIONS WITH TEST (ADD, DELETE, CHANGE) -------------------------------------- #		
def add_test(request):
	"""Register a new test."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo.add_test"):
			if request.method == 'POST':
				form = TestForm(request.POST)
				if form.is_valid():
					result = form.save(request.POST, request.user)
					if result == True:
						form = TestForm()
						msg = configuration.TEST_ADD_SUCESSFULLY
						return render_to_response("add_test.html", {'form' : form, 'msg' : msg, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
					else:
						form = TestForm()
						error = configuration.TEST_EXISTS
						return render_to_response("add_test.html.html", {'form' : form, 'error' : error, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
				else:
					error = configuration.TEST_ADD_ERROR
					form = TestForm()
					return render_to_response("add_test.html", {'form' : form, 'error':error, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
			else:
				form = TestForm()
				return render_to_response('add_test.html', {'form': form, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
		else:
			error = configuration.TESTS_ADD_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
	
def change_test(request, test_id):
	"""Change the contend of test represented by test_id."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo.change_test"):
			t = queries.get_test(test_id)
			if request.method == 'POST':
				util.change_test(t, request.POST['contend'])
				t.code = contend
				t.save()
				msg = configuration.TEST_UPDATE_SUCESS
				util.register_action(request.user, configuration.LOG_EDIT_TEST % t.name)
				exs = Exercise.objects.all()
				return render_to_response("update_test.html", {'msg': msg, 'test':t, 'exercises': exs, 'contend':contend, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
			else:
				contend = t.code
				exs = Exercise.objects.all()
				return render_to_response("update_test.html", {'test': t, 'exercises': exs, 'contend':contend, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
		else:
			error = configuration.TEST_UPDATE_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:	
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
	
def under_test(request, test_id):
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo.change_test"):
			original_test = queries.get_test(test_id)
			exercise = queries.get_exercise(original_test.exercise.id)
			under_test = UnderTest().create_test(request.user, exercise, request.POST['contend'])
			util.save_under_test_file(under_test)
			under_test.save()
			original_test.locked = True
			original_test.save()
			
			form = ChoiceSubmissionsForm(exercise.id)
			msg = configuration.UNDER_TEST_ADD_SUCESSFULLY
			return render_to_response("choice_submissions.html", {'form' : form, 'exercise':exercise, 'msg': msg, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
		else:
			error = configuration.TEST_UPDATE_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:	
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
	
def choice_submissions(request, exercise_id):
	pass
	
def test_view(request, test_id):
	"""View that shows test details."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo.see_tests"):
			if request.method == 'GET':
				test = queries.get_test(test_id)
				lines = test.code
				exercise = queries.get_exercise(test.exercise.id)
				return render_to_response("test_view.html", {'exercise': exercise, 'test':test, 'code': lines, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
		else:
			error = configuration.TEST_SEE_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))


def annul_test(request, test_id):
	"""View invoked when the action of annul a test is actioned."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo.invalidate_tests"):
			if request.method == 'POST':
				test = queries.get_test(test_id)
				path = test.path
				exercise = queries.get_exercise(test.exercise.id)
				file = open(settings.MEDIA_ROOT + '/tests/' + configuration.BACKUP_TEST_NAME + '_' + exercise.name + '.py', 'rb')
				os.remove(settings.MEDIA_ROOT + '/tests/' + path)
				
				recovered_file = open(settings.MEDIA_ROOT + '/tests/' + path, 'wb')
				recovered_file.write(file.read())
				recovered_file.close()
				
				students = queries.get_all_students()
				for s in students:
					usr = s.username
					path_student = settings.MEDIA_ROOT + '/' + usr + '/' + path
					os.remove(path_student)
					r_file = open(path_student, 'wb')
					r_file.write(file.read())
					r_file.close()
				
				lines = open(settings.MEDIA_ROOT + '/tests/' + path).read()
				util.register_action(request.user, configuration.LOG_IVALIDATE_TEST % test.name)
				
				return render_to_response("test_view.html", {'exercise':exercise, 'test':test, 'code': lines, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
		else:
			error = configuration.INVALIDATE_TEST_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
		
def tests(request):
	"""List all tests."""
	
	if request.user.is_authenticated():
		if request.method == 'GET':
			tests = queries.get_all_tests()
			return render_to_response("tests.html", {'tests' : tests, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
	else:	
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
