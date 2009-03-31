# coding: utf-8

#Hoopaloo - Version 1.0 - 2008/2009
#Author: Mariana Romao do Nascimento - mariana@dsc.ufcg.edu.br

from django.http import HttpResponse
from django.shortcuts import render_to_response

def help_index(request):
	if request.user.is_authenticated():
		return render_to_response("help/index.html")
		
def help_index_student(request):
	if request.user.is_authenticated():
		return render_to_response("help/index_student.html")	
		
def help_login(request):
	if request.user.is_authenticated():
		return render_to_response("help/login.html")
		
def help_forgot_password(request):
	if request.user.is_authenticated():
		return render_to_response("help/forgot_password.html")
		
def help_change_password(request):
	if request.user.is_authenticated():
		return render_to_response("help/change_password.html")
		
def help_register_student(request):
	if request.user.is_authenticated():
		return render_to_response("help/register_student.html")

def help_register_assistant(request):
	if request.user.is_authenticated():
		return render_to_response("help/register_assistant.html")
		
def help_assign(request):
	if request.user.is_authenticated():
		return render_to_response("help/assign_students.html")
		
def help_register_exercise(request):
	if request.user.is_authenticated():
		return render_to_response("help/register_exercise.html")

def help_register_test(request):
	if request.user.is_authenticated():
		return render_to_response("help/register_test.html")
		
def help_edit_exercise(request):
	if request.user.is_authenticated():
		return render_to_response("help/edit_exercise.html")
		
def help_edit_test(request):
	if request.user.is_authenticated():
		return render_to_response("help/edit_test.html")
		
def help_list_exercises(request):
	if request.user.is_authenticated():
		return render_to_response("help/list_exercises.html")
		
def help_list_tests(request):
	if request.user.is_authenticated():
		return render_to_response("help/list_tests.html")
		
def help_exercise_view(request):
	if request.user.is_authenticated():
		return render_to_response("help/exercise_view.html")
		
def help_test_view(request):
	if request.user.is_authenticated():
		return render_to_response("help/test_view.html")
		
def help_students_view(request):
	if request.user.is_authenticated():
		return render_to_response("help/students_view.html")
		
def help_exercises_student(request):
	if request.user.is_authenticated():
		return render_to_response("help/exercises_student.html")
		
def help_submission(request):
	if request.user.is_authenticated():
		return render_to_response("help/submission.html")
	
def help_submission_view(request):
	if request.user.is_authenticated():
		return render_to_response("help/submission_view.html")
		
def help_student_initial_page(request):
	if request.user.is_authenticated():
		return render_to_response("help/student_initial_page.html")
		
def help_assistant_initial_page(request):
	if request.user.is_authenticated():
		return render_to_response("help/assistant_initial_page.html")

def help_test_percentage(request):
	if request.user.is_authenticated():
		return render_to_response("help/test_percentage.html")
		
def help_note_percentual(request):
	if request.user.is_authenticated():
		return render_to_response("help/note_percentual.html")
		
def help_user_details(request):
	if request.user.is_authenticated():
		return render_to_response("help/user_details.html")
		
def help_actions_log(request):
	if request.user.is_authenticated():
		return render_to_response("help/actions_log.html")
