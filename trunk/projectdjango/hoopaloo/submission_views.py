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
import queries
import configuration


# --------------------------------------------- OPERATIONS WITH SUBMISSION ----------------------------- #
def submission(request):
	"""Redirect to page to submit solutions."""
	
	if request.user.is_authenticated():
		if request.user.has_perm("hoopaloo.add_submission"):
			explication = configuration.SUBMISSION_MSG
			student = queries.get_student_from_user_id(request.user.id)
			if request.method == 'POST':
				form = SubmissionForm(request.POST, request.FILES)
				if form.is_valid():
					result = form.save(request)
					form = SubmissionForm()
					r, msg = util.make_message_student(result)
					submissions = queries.get_student_submissions(student.id)
					if r:
						return render_to_response("submission.html", {'form' : form, 'msg' : msg, 'submissions':submissions, 'student': student,}, context_instance=RequestContext(request))
					else:
						return render_to_response("submission.html", {'form' : form, 'error' : msg, 'explication':explication, 'submissions':submissions, 'student': student, }, context_instance=RequestContext(request))
				else:
					form = SubmissionForm() 
					error = []
					error.append(configuration.SUBMISSION_ERROR)
					return render_to_response('submission.html', {'form': form, 'explication':explication, 'error':error, 'submissions': submissions, 'student': student,}, context_instance=RequestContext(request))
			else:
				submissions = queries.get_student_submissions(student.id)
				form = SubmissionForm() 
				return render_to_response('submission.html', {'form': form, 'explication':explication, 'submissions':submissions, 'student': student,}, context_instance=RequestContext(request))
		else:
			error = configuration.SUBMISSION_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
		
def view_code(request, submission_id, student_id):
	if request.user.is_authenticated():
		try:
			profile = request.user.get_profile()
		except:
			pass
		if request.user.has_perm(".see_submission"):
			
			if request.user.is_superuser or isinstance(profile, Assistant) or (long(profile.id) == long(student_id)):
				submission = queries.get_submission(submission_id)
				file = open(submission.solution_file.name, 'rb')
				codelines = util.remove_acentuation(file.read())			
				response = HttpResponse(codelines)
				response["Content-Type"] = "text/x-python"
				return response
			else:
				error = configuration.SUBMISSION_SEE_NOT_PERMISSION
				return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))				
		else:
			error = configuration.SUBMISSION_SEE_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))
		
def see_submissions(request):
	if request.user.is_authenticated():
		if request.user.has_perm(".see_submission"):
			student = queries.get_student_from_user_id(request.user.id)
			submissions = queries.get_ordered_student_submissions(id_student=student.id)
			explication = configuration.REALIZED_SUBMISSIONS
			return render_to_response("student_initial_page.html", { 'student':student, 'submissions':submissions, 'explication':explication,}, context_instance=RequestContext(request))
		else:
			error = configuration.SUBMISSION_SEE_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))

def view_exercise(request, submission_id, exercise_id, student_id=None):
	""""Shows submission details of student represented by student_id for the exercise represented by exercise_id."""
	
	if request.user.is_authenticated():
		if request.user.has_perm(".see_submission"):
			profile = None
			try:
				profile = request.user.get_profile()
			except:
				pass
			exercise = queries.get_exercise(exercise_id)
			sub = queries.get_submission(submission_id)
			student = queries.get_student(sub.id_student.id)
			result = None
			execution = None
			try:
				#TODO DUVIDA AQUI... EH A ULTIMA EXECUCAO???
				execution = Execution.objects.get(id_submission=sub.id, id_student=student.id)
			except:
				# The File was not executed
				pass
			arq = open(sub.solution_file.name)
			aux = arq.read()
			cde = util.remove_acentuation(aux)
			lines = aux.count('\n') + 3
			arq.close()
			t = None
			try:
				t = queries.get_consolidated_test(exercise.id)
			except:
				pass
			
			if request.method == 'GET':
				if (request.user.is_superuser or isinstance(profile, Assistant)):
					student = queries.get_student(student_id)
					return render_to_response("submission_view_t.html", {'exercise' : exercise, 'code':cde, 'student':student, 'test': t, 'lines':lines, 'submission': sub, 'execution':execution, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
				
				elif isinstance(profile, Student):
					# security against students that want to see the friend's code
					if long(profile.id) == long(student_id):
						return render_to_response("submission_view_s.html", {'exercise' : exercise, 'code':cde, 'execution': execution, 'submission': sub, 'lines':lines, }, context_instance=RequestContext(request))
					else:
						error = configuration.SUBMISSION_SEE_NOT_PERMISSION
						return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
			else:
				has_error, error = util.add_score_and_comments(request.POST['comments'], request.POST['score'], exercise, sub)
				util.register_action(request.user, configuration.LOG_EDIT_SUBMISSION % (sub.id, student.username))
				
				if not has_error:
					msg = configuration.ADD_COMMENT_SCORE_SUCESS
					return render_to_response("submission_view_t.html", {'msg': msg, 'exercise' : exercise,  'student':student, 'submission': sub, 'code':cde, 'execution':execution, 'is_assistant': util.is_assistant(request.user),}, context_instance=RequestContext(request))
				else:
					return render_to_response("submission_view_t.html", {'exercise' : exercise, 'student':student, 'submission': sub, 'code':cde, 'execution':execution, 'error': error, 'is_assistant': util.is_assistant(request.user)}, context_instance=RequestContext(request))
		else:
			error = configuration.SUBMISSION_SEE_NOT_PERMISSION
			return render_to_response("error_page.html", {'error' : error}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		return render_to_response("login.html", {'form' : form}, context_instance=RequestContext(request))

