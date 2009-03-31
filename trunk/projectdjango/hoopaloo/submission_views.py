# coding: utf-8

#Hoopaloo - Version 1.0 - 2008/2009
#Author: Mariana Romao do Nascimento - mariana@dsc.ufcg.edu.br

from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib import auth
from django.conf import settings
from projectdjango.hoopaloo.models import *
from projectdjango.hoopaloo.forms import *
import util
from hoopaloo import configuration


# --------------------------------------------- OPERATIONS WITH SUBMISSION ----------------------------- #
def submission(request):
	"""Redirect to page to submit solutions."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo.add_submission"):
			explication = configuration.SUBMISSION_MSG
			if request.method == 'POST':
				form = SubmissionForm(request.POST, request.FILES)
				if form.is_valid():
					result = form.save(request)
					form = SubmissionForm()
					r, msg = util.make_message_student(result)
					student = Student.objects.get(user=request.user.id)
					submissions = Submission.objects.filter(id_student=student.id)
					if r:
						return render_to_response("submission.html", {'form' : form, 'msg' : msg, 'submissions':submissions, 'student': student,}, context_instance=RequestContext(request))
					else:
						return render_to_response("submission.html", {'form' : form, 'error' : msg, 'explication':explication, 'submissions':submissions, 'student': student, }, context_instance=RequestContext(request))
				else:
					form = SubmissionForm() 
					error = []
					error.append(configuration.SUBMISSION_ERROR)
					return render_to_response('submission.html', {'form': form, 'explication':explication, 'error':error, }, context_instance=RequestContext(request))
			else:
				student = Student.objects.get(user=request.user.id)
				submissions = Submission.objects.filter(id_student=student.id)
				form = SubmissionForm() 
				return render_to_response('submission.html', {'form': form, 'explication':explication, 'submissions':submissions}, context_instance=RequestContext(request))
		else:
			error = configuration.SUBMISSION_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
		
def view_code(request, submission_id, student_id):
	if request.user.is_authenticated():
		profile = request.user.get_profile()
		if request.user.has_perm(".see_submission") and (long(profile.id) == long(student_id)):
			submission = Submission.objects.get(pk=submission_id, id_student=student_id)
			file = open(submission.solution_file.name, 'rb')
			codelines = util.remove_acentuation(file.read())
			return render_to_response("submission_code.html", {'codelines':codelines, }, context_instance=RequestContext(request))
		else:
			error = configuration.SUBMISSION_SEE_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
		
def see_submissions(request):
	if request.user.is_authenticated():
		if request.user.has_perm(".see_submission"):
			student = Student.objects.get(user=request.user.id)
			submissions = Submission.objects.filter(id_student=student.id).order_by('date').reverse()
			explication = configuration.REALIZED_SUBMISSIONS
			return render_to_response("student_initial_page.html", { 'student':student, 'submissions':submissions, 'explication':explication,}, context_instance=RequestContext(request))
		else:
			error = configuration.SUBMISSION_SEE_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
	
	
def submissions_student(request):
	if request.user.is_authenticated():
		if request.user.has_perm(".see_submission"):
			pass
		else:
			error = configuration.SUBMISSION_SEE_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))

def view_exercise(request, exercise_id, student_id=None):
	""""Shows submission details of student represented by student_id for the exercise represented by exercise_id."""
	
	if request.user.is_authenticated():
		if request.user.has_perm(".see_submission"):
			profile = None
			try:
				profile = request.user.get_profile()
			except:
				pass
			exercise = Exercise.objects.get(id=exercise_id)
			submissions = Submission.objects.filter(id_exercise=exercise_id, id_student=student_id).order_by('date')
			
			if submissions.count() > 0 :
				s = submissions[len(submissions)-1]
				student = Student.objects.get(pk=s.id_student.id)
				result = None
				try:
					result = Result.objects.get(id_exercise=exercise_id, id_student=student_id)
				except:
					# The File was not executed
					pass
				arq = open(s.solution_file.name)
				cde = arq.read()
				lines = cde.count('\n') + 3
				arq.close()
				t = None
				try:
					t = Test.objects.get(exercise=exercise.id)
				except:
					pass
				
				if request.method == 'GET':
					if (request.user.is_superuser or isinstance(profile, Assistant)):
						student = Student.objects.get(pk=student_id)
						executions = Execution.objects.filter(id_submission=s.id, id_student=student.id).order_by('date').reverse()
						execution = executions[0]
						return render_to_response("submission_view_t.html", {'exercise' : exercise, 'result':result, 'code':cde, 'student':student, 'test': t, 'lines':lines, 'execution':execution, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
					
					elif isinstance(profile, Student):
						# security against students that want to see the friend's code
						if long(profile.id) == long(student_id):
							return render_to_response("submission_view_s.html", {'exercise' : exercise, 'result':result, 'code':cde, 'lines':lines, }, context_instance=RequestContext(request))
						else:
							error = configuration.SUBMISSION_SEE_NOT_PERMISSION
							return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
				else:
					has_error, error = util.add_score_and_comments(request.POST['comments'], request.POST['score'], exercise, s)
					util.register_action(request.user, configuration.LOG_EDIT_SUBMISSION % (s.id, student.username))
					
					if not has_error:
						return render_to_response("submission_view_t.html", {'exercise' : exercise, 'result':result, 'code':cde, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
					else:
						return render_to_response("submission_view_t.html", {'exercise' : exercise, 'result':result, 'code':cde, error: error, }, context_instance=RequestContext(request))
			else:
				if (request.user.is_superuser or isinstance(profile, Assistant)):
					return render_to_response("submission_view_t.html", {'exercise' : exercise, })
				return render_to_response("submission_view_s.html", {'exercise' : exercise,}, context_instance=RequestContext(request))
		else:
			error = configuration.SUBMISSION_SEE_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))

