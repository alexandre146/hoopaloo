# coding: utf-8

#Hoopaloo - Version 1.0 - 2008/2009
#Author: Mariana Romao do Nascimento - mariana@dsc.ufcg.edu.br

from projectdjango.hoopaloo.models import Student, Assistant
from projectdjango.hoopaloo.forms import RegisterAssistantForm, RegisterStudentForm, LoginForm, AssignStudentsForm
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib import auth
from django.conf import settings
import util
from hoopaloo import configuration

# ----------------------  OPERATIONS WITH USERS (ADD STUDENT< ASSISTANT, DELETE STUDENT, ASSISTANT, SEE USER INFORMATIONS) ---------------------------- #

# Register an new assistant
def register_assistant(request):
	"""Add a new assistant to the system."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo.add_assistant"):
			if request.method == 'POST':
				form = RegisterAssistantForm(request.POST)
				errors = form.save(request)
				if (len(errors)==0):
					form = RegisterAssistantForm()
					msg = configuration.ASSISTANT_ADD_SUCESS
					return render_to_response("register_assistant.html", {'form':form, 'msg':msg, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
				else:
					error = configuration.ASSISTANT_ADD_ERROR
					form = RegisterAssistantForm(errors)
					return render_to_response("register_assistant.html", {'form' : form, 'error':error, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
			else:
				form = RegisterAssistantForm()
				return render_to_response("register_assistant.html", {'form' : form, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
		else:
			error = configuration.ASSISTANT_ADD_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error, }, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))


# Register a new student
def register_student(request):
	""""Add a new student to the system."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo.add_student"):
			if request.method == 'POST':
				form = RegisterStudentForm(request.POST)
				if form.is_valid():
					errors = form.save(request)
					if (len(errors)==0):
						form = RegisterStudentForm()
						msg = configuration.STUDENT_ADD_SUCESS
						return render_to_response("register_student.html", {'form' : form, 'msg':msg, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
					else:
						error = configuration.STUDENT_ADD_ERROR
						form = RegisterStudentForm(errors)
						return render_to_response("register_student.html", {'form' : form, 'error':error, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
				else:
					error = configuration.STUDENT_ADD_ERROR
					return render_to_response("register_student.html", {'form' : form, 'error':error, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
			else:
				form = RegisterStudentForm()
				return render_to_response("register_student.html", {'form' : form, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
		else:
			error = configuration.STUDENT_ADD_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))			
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
		
def users(request):
	"""View to see all informations about the users."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo.see_users"):
			students = Student.objects.all().order_by('username')
			assistants = Assistant.objects.all().order_by('username')
				
			return render_to_response("users.html", {'students' : students, 'assistants': assistants, 'is_assistant': util.is_assistant(request.user), }, context_instance=RequestContext(request))
		else:
			error = confguration.VIEW_USERS_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:	
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
		
def delete_users(request, user_id):
	"""Views called when the delete user action is actionde."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo.delete_user"):
			user = User.objects.get(pk=user_id)
			return render_to_response("delete_user.html", {'user':user,}, context_instance=RequestContext(request))
		else:
			error = confguration.DELETE_USERS_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:	
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
		
def delete_user(request, user_id):
	"""Redirect to a confirmation page before delete the user."""
	
	if request.user.is_authenticated():
		if request.method == 'GET':
			return render_to_response("delete_user.html", {'method':request.method,},  context_instance=RequestContext(request))
		else:
			# deleting the user
			user = User.objects.get(pk=user_id)
			profile = user.get_profile()
			profile.delete()
			user.delete()
			
			msg = configuration.USER_DELETED
			util.register_action(request.user, configuration.LOG_DELETE_USER % user.username)	
			return render_to_response("delete_user.html", {'method':request.method, 'msg':msg,}, context_instance=RequestContext(request))
	else:	
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))

# ------------------------------------------------- ASSIGN STUDENTS TO ASSISTANTS -------------------------------------------------------- #
def assign_students(request):
	"""Assign students to assistants."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo.assign_student"):
			if request.method == 'POST':
				form = AssignStudentsForm(request.POST)
				errors = form.save(request)
				if (len(errors)==0):
					form = AssignStudentsForm()
					msg = configuration.ASSIGN_SUCESS
					return render_to_response("assign_students.html", {'form':form, 'msg':msg, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
				else:
					error = configuration.REVIEW_ASSIGN
					form = AssignStudentsForm(errors)
					return render_to_response("assign_students.html", {'form' : form, 'error':error, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
			else:
				form = AssignStudentsForm()
				return render_to_response("assign_students.html", {'form' : form, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
		else:
			error = configuration.ASSIGN_STUDENTS_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
		
def assigns(request):
	"""Redirect to a page with all assigns between assitants and students."""
	
	if request.user.is_authenticated():
		if request.method == 'GET':
			students = Student.objects.all()
			assistants = Assistant.objects.all()
			return render_to_response('assigns.html', {'students':students, 'assistants':assistants, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
			
