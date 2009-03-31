# coding: utf-8

#Hoopaloo - Version 1.0 - 2008/2009
#Author: Mariana Romao do Nascimento - mariana@dsc.ufcg.edu.br

from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib import auth
from projectdjango.hoopaloo.models import Student, Submission, Assistant, Class
from projectdjango.hoopaloo.forms import LoginForm, ForgotPasswordForm, ChangePasswordForm
from hoopaloo import configuration
import util

# This view makes the login of an user and redirect him/her to student's view or teacher's view or assistant view

def login(request):
	"""The function view responsible by user login.
	If the user already logged redirect to initial page, if not realize the login
	and redirect to initial page."""
	
	if not request.user.is_authenticated():
		form = LoginForm()
		if request.method == 'POST':
			usrname = request.POST['username']
			pword = request.POST['password']
			user = auth.authenticate(username=usrname, password=pword)
			if user and user.is_active:
				# Correct password, and the user is marked "active"
				auth.login(request, user)
				
				#the user's session cookie will expire when the user's Web browser is closed
				request.session.set_expiry(0)
				# register the action
				util.register_action(user, configuration.LOG_LOGIN)
				# Redirect to a specific page
				if user.is_superuser:
					classes = Class.objects.filter(teacher=user.id)
					s = []
					for c in classes:
						students = Student.objects.filter(student_class=c.id)
						for st in students:
							s.append(st)
					return render_to_response("teacher_view.html", {'students': s, 'user': user,  }, context_instance=RequestContext(request))
				else:
					if util.first_access(user) == False:
						try:
							# trying recover a student profile
							profile = Assistant.objects.get(user=request.user.id)
						except:
							# trying recover a assistant profile
							profile = Student.objects.get(user=request.user.id)
						if isinstance(profile, Assistant):
							students = Student.objects.filter(assistant=profile.id)
							return render_to_response("assistant_view.html", {'students': students, 'user': user, }, context_instance=RequestContext(request))
						else:
							submissions = Submission.objects.filter(id_student=profile.id).order_by('date').reverse()
							explication = configuration.REALIZED_SUBMISSIONS
							return render_to_response("student_initial_page.html", { 'student':profile, 'submissions':submissions, 'explication':explication,}, context_instance=RequestContext(request))
					else:
						form = ChangePasswordForm()
						return render_to_response("change_password.html", {'form': form, }, context_instance=RequestContext(request))
			else:
				# Show an message of error at the login page
				errors = 'Error'
				return render_to_response("login.html", {'errors': errors, 'form': form, }, context_instance=RequestContext(request))
		else:
			form = LoginForm() # An unbound form
			return render_to_response('login.html', {'form': form,}, context_instance=RequestContext(request))
	else:
		msg = configuration.LOGIN_SUCESS
		user = request.user
		if user.is_superuser:
			students = Student.objects.all()
			return render_to_response("teacher_view.html", {'students': students, 'user': user, 'msg':msg,}, context_instance=RequestContext(request))
		else:
			profile = user.get_profile()
			if isinstance(profile, Assistant):
				students = Student.objects.filter(assistant=profile.id)
				return render_to_response("assistant_view.html", {'students': students, 'user': user, 'msg':msg,}, context_instance=RequestContext(request))
			elif isinstance(profile, Student):
				submissions = Submission.objects.filter(id_student=profile.id).order_by('date').reverse()
				explication = configuration.REALIZED_SUBMISSIONS
				return render_to_response("student_initial_page.html", { 'student':profile, 'submissions':submissions, 'explication':explication,}, context_instance=RequestContext(request))
					
		
# This view makes the logout of an user
def logout(request):
	"""The funtion view responsible by logout."""
	
	if request.user.is_authenticated():
		util.register_action(request.user, configuration.LOG_LOGOUT)
		auth.logout(request)
		request.session.flush()
		# Redirect to initial page.
		form = LoginForm()
		msg = configuration.LOGOUT_SUCESS
		return render_to_response('login.html', {'form': form, 'msg': msg,}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response('login.html', {'form': form,}, context_instance=RequestContext(request))
		
def change_password(request):
	"""Modify the password of an user."""
	
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = ChangePasswordForm(request.POST)
			if form.is_valid():
				if request.user.check_password(request.POST['old_password']):
					# testing if the password and password retype are equals
					if request.POST['password1'] == request.POST['password2']:
						new_pwd = request.POST['password1']
						user = request.user
						#setting the new password
						user.set_password(new_pwd)
						user.save()
						form = LoginForm()
						msg = configuration.PASSWORD_CHANGED_MSG
						util.register_action(user, configuration.LOG_CHANGE_PASSWORD)
						auth.logout(request)
						try:
							profile = user.get_profile()
							profile.realized_login = True
							profile.save()
						except:
							pass
						return render_to_response("login.html", {'form': form, 'msg':msg,}, context_instance=RequestContext(request))
					else:
						# the password and the password retype did not matches
						error = configuration.PASSWORD_NOT_MATCHES
						form = ChangePasswordForm()
						return render_to_response("change_password.html", {'form': form, 'error':error,},context_instance=RequestContext(request))
				else:
					# the old password is wrong
					error = configuration.INVALID_PASSWORD
					form = ChangePasswordForm()
					return render_to_response("change_password.html", {'form': form, 'error':error,}, context_instance=RequestContext(request))
			else:
				# the password has invalid characters 
				error = configuration.INVALID_PASSWORD
				form = ChangePasswordForm()
				return render_to_response("change_password.html", {'form': form, 'error':error,}, context_instance=RequestContext(request))
		else:
			form = ChangePasswordForm()
			return render_to_response("change_password.html", {'form': form, }, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response('login.html', {'form': form,}, context_instance=RequestContext(request))	

def forgot_password(request):
	"""This function is called when the user forgot his/hers password.
	A new password is generated and sended by email to the user."""
	
	form = ForgotPasswordForm()
	if request.method == 'POST':
		form = ForgotPasswordForm(request.POST)
		if form.is_valid():
			e = request.POST['email']
			try:
				user = User.objects.filter(email=e)[0]
				# generate the new password and send to email
				util.send_new_password(e, user)
				form = LoginForm()
				util.register_action(user, configuration.LOG_FORGOT_PASSWORD % e )
				return render_to_response("login.html", {'form': form,}, context_instance=RequestContext(request))
			except:
				errors = configuration.FORGOT_PASSWORD
				return render_to_response("forgot_password.html", {'errors': errors, 'form': form, }, context_instance=RequestContext(request))
		else:
			return render_to_response("forgot_password.html", {'form': form, }, context_instance=RequestContext(request))	
	else:
		form = ForgotPasswordForm()
		return render_to_response('forgot_password.html', {'form': form,}, context_instance=RequestContext(request))
