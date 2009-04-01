# coding: utf-8

#Hoopaloo - Version 1.0 - 2008/2009
#Author: Mariana Romao do Nascimento - mariana@dsc.ufcg.edu.br

from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
	
	#AUTENTICATION_VIEWS
	(r'^hoopaloo/$', 'projectdjango.hoopaloo.autentication_views.login'),
	(r'^hoopaloo/logout/$', 'projectdjango.hoopaloo.autentication_views.logout'),
	(r'^hoopaloo/forgot_password/$', 'projectdjango.hoopaloo.autentication_views.forgot_password'),
    (r'^admin/(.*)', admin.site.root),
	(r'^hoopaloo/login/$', 'projectdjango.hoopaloo.autentication_views.login'),
	(r'^hoopaloo/.*/logout/$', 'projectdjango.hoopaloo.autentication_views.logout'),
	(r'^hoopaloo/.*/password_change/$', 'projectdjango.hoopaloo.autentication_views.change_password'),
	(r'^hoopaloo/change_password/$', 'projectdjango.hoopaloo.autentication_views.change_password'),
	
	# USERS_VIEWS
	(r'^hoopaloo/register_student/$', 'projectdjango.hoopaloo.users_views.register_student'),
	(r'^hoopaloo/register_assistant/$', 'projectdjango.hoopaloo.users_views.register_assistant'),
	(r'^hoopaloo/delete_users/id=(?P<user_id>\d+)/$', 'projectdjango.hoopaloo.users_views.delete_users'),
	(r'^hoopaloo/delete_user/id=(?P<user_id>\d+)/$', 'projectdjango.hoopaloo.users_views.delete_user'),
	(r'^hoopaloo/users/$', 'projectdjango.hoopaloo.users_views.users'),
	(r'^hoopaloo/assign_students/$', 'projectdjango.hoopaloo.users_views.assign_students'),
	(r'^hoopaloo/assigns/$', 'projectdjango.hoopaloo.users_views.assigns'),
	(r'^hoopaloo/delete_assign/id=(?P<student_id>\d+)/$', 'projectdjango.hoopaloo.users_views.delete_assign'),
	
	# GENERAL VIEWS
	(r'^hoopaloo/actions/$', 'projectdjango.hoopaloo.views.actions'),
	(r'^hoopaloo/assistant_view/$', 'projectdjango.hoopaloo.views.assistant_view'),
	(r'^hoopaloo/global_assistant_view/$', 'projectdjango.hoopaloo.views.global_assistant_view'),
	(r'^hoopaloo/teacher_view/$', 'projectdjango.hoopaloo.views.teacher_view'),
	(r'^hoopaloo/all_students/$', 'projectdjango.hoopaloo.views.all_students'),
	(r'^hoopaloo/delivered_exercises/$', 'projectdjango.hoopaloo.views.delivered_exercises'),
	(r'^hoopaloo/delivered_exercises/student/id=(?P<student_id>\d+)$', 'projectdjango.hoopaloo.views.delivered_exercises_student'),
	(r'^hoopaloo/undelivered_exercises/$', 'projectdjango.hoopaloo.views.undelivered_exercises'),
	(r'^hoopaloo/available_exercises/$', 'projectdjango.hoopaloo.views.available_exercises'),
	(r'^hoopaloo/exercise/percentual/id=(?P<exercise_id>\d+)$', 'projectdjango.hoopaloo.views.exercise_percentual'),
	(r'^hoopaloo/exercise/score_percentual/id=(?P<exercise_id>\d+)$', 'projectdjango.hoopaloo.views.score_percentual'),
	(r'^hoopaloo/exercises/student/id=(?P<student_id>\d+)$', 'projectdjango.hoopaloo.views.student_exercises'),
	(r'^hoopaloo/list_percentual(?P<percent>\d+)/id=(?P<id_exercise>\d+)$', 'projectdjango.hoopaloo.views.list_percentual'),
	(r'^hoopaloo/list_score_percentual(?P<index>\d+)/id=(?P<id_exercise>\d+)$', 'projectdjango.hoopaloo.views.list_score_percentual'),
	
	# EXERCISE_VIEWS
	(r'^hoopaloo/add_exercise/$', 'projectdjango.hoopaloo.exercise_views.add_exercise'),
	(r'^hoopaloo/exercises/$', 'projectdjango.hoopaloo.exercise_views.exercises'),
	(r'^hoopaloo/exercises/id=(?P<id_exercise>\d+)/$', 'projectdjango.hoopaloo.exercise_views.exercises'),
	(r'^hoopaloo/change_exercise/id=(?P<exercise_id>\d+)/$', 'projectdjango.hoopaloo.exercise_views.change_exercise'),
	(r'^hoopaloo/exercise/id=(?P<exercise_id>\d+)/$', 'projectdjango.hoopaloo.exercise_views.exercise'),
	(r'^hoopaloo/change_exercise/id=(?P<exercise_id>\d+)$', 'projectdjango.hoopaloo.exercise_views.change_exercise'),
	(r'^hoopaloo/delete_exercises/id=(?P<exercise_id>\d+)/$', 'projectdjango.hoopaloo.exercise_views.delete_exercises'),
	(r'^hoopaloo/delete_exercise/id=(?P<exercise_id>\d+)/$', 'projectdjango.hoopaloo.exercise_views.delete_exercise'),
	(r'^hoopaloo/change_availability_exercise/id=(?P<id_exercise>\d+)/$', 'projectdjango.hoopaloo.exercise_views.change_availability_exercise'),
	(r'^hoopaloo/availability_exercise/id=(?P<id_exercise>\d+)/$', 'projectdjango.hoopaloo.exercise_views.availability_exercise'),
	
	# TEST_VIEWS
	(r'^hoopaloo/tests/$', 'projectdjango.hoopaloo.test_views.tests'),
	(r'^hoopaloo/add_test/$', 'projectdjango.hoopaloo.test_views.add_test'),
	(r'^hoopaloo/change_test/id=(?P<test_id>\d+)/$', 'projectdjango.hoopaloo.test_views.change_test'),
	(r'^hoopaloo/change_test/id=(?P<test_id>\d+)$', 'projectdjango.hoopaloo.test_views.change_test'),
	(r'^hoopaloo/test_view/id=(?P<test_id>\d+)$', 'projectdjango.hoopaloo.test_views.test_view'),
	(r'^hoopaloo/annul_test/id=(?P<test_id>\d+)/$', 'projectdjango.hoopaloo.test_views.annul_test'),

	# SUBMISSION_VIEWS
	(r'^hoopaloo/submission/$', 'projectdjango.hoopaloo.submission_views.submission'),
	(r'^hoopaloo/submission(?P<submission_id>\d+)/student(?P<student_id>\d+)/exercise/id=(?P<exercise_id>\d+)$', 'projectdjango.hoopaloo.submission_views.view_exercise'),
	(r'^hoopaloo/submission(?P<submission_id>\d+)/student(?P<student_id>\d+)/exercise/id=(?P<exercise_id>\d+)/$', 'projectdjango.hoopaloo.submission_views.view_exercise'),
	(r'^hoopaloo/submission(?P<submission_id>\d+)/student(?P<student_id>\d+)/$', 'projectdjango.hoopaloo.submission_views.view_code'),
	(r'^hoopaloo/see_submissions/$', 'projectdjango.hoopaloo.submission_views.see_submissions'),
	#(r'^hoopaloo/submissions/student(?P<student_id>\d+)/$', 'projectdjango.hoopaloo.submission_views.submissions_student'),
	
	# HELPS
	(r'^hoopaloo/help$', 'projectdjango.hoopaloo.help_views.help_index'),
	(r'^hoopaloo/help_student$', 'projectdjango.hoopaloo.help_views.help_index_student'),
	(r'^hoopaloo/help/login$', 'projectdjango.hoopaloo.help_views.help_login'),
	(r'^hoopaloo/help/register_student$', 'projectdjango.hoopaloo.help_views.help_register_student'),
	(r'^hoopaloo/help/register_assistant$', 'projectdjango.hoopaloo.help_views.help_register_assistant'),
	(r'^hoopaloo/help/register_exercise$', 'projectdjango.hoopaloo.help_views.help_register_exercise'),
	(r'^hoopaloo/help/register_test$', 'projectdjango.hoopaloo.help_views.help_register_test'),
	(r'^hoopaloo/help/assign$', 'projectdjango.hoopaloo.help_views.help_assign'),
	(r'^hoopaloo/help/change_password$', 'projectdjango.hoopaloo.help_views.help_change_password'),
	(r'^hoopaloo/help/forgot_password$', 'projectdjango.hoopaloo.help_views.help_forgot_password'),
	(r'^hoopaloo/help/edit_exercise$', 'projectdjango.hoopaloo.help_views.help_edit_exercise'),
	(r'^hoopaloo/help/edit_test$', 'projectdjango.hoopaloo.help_views.help_edit_test'),
	(r'^hoopaloo/help/list_exercises$', 'projectdjango.hoopaloo.help_views.help_list_exercises'),
	(r'^hoopaloo/help/list_tests$', 'projectdjango.hoopaloo.help_views.help_list_tests'),
	(r'^hoopaloo/help/exercise_view$', 'projectdjango.hoopaloo.help_views.help_exercise_view'),
	(r'^hoopaloo/help/test_view$', 'projectdjango.hoopaloo.help_views.help_test_view'),
	(r'^hoopaloo/help/students_view$', 'projectdjango.hoopaloo.help_views.help_students_view'),
	(r'^hoopaloo/help/exercises_student$', 'projectdjango.hoopaloo.help_views.help_exercises_student'),
	(r'^hoopaloo/help/submission$', 'projectdjango.hoopaloo.help_views.help_submission'),
	(r'^hoopaloo/help/submission_view$', 'projectdjango.hoopaloo.help_views.help_submission_view'),
	(r'^hoopaloo/help/student_initial_page$', 'projectdjango.hoopaloo.help_views.help_student_initial_page'),
	(r'^hoopaloo/help/assistant_initial_page$', 'projectdjango.hoopaloo.help_views.help_assistant_initial_page'),
	(r'^hoopaloo/help/test_percentage$', 'projectdjango.hoopaloo.help_views.help_test_percentage'),
	(r'^hoopaloo/help/note_percentual$', 'projectdjango.hoopaloo.help_views.help_note_percentual'),
	(r'^hoopaloo/help/user_details$', 'projectdjango.hoopaloo.help_views.help_user_details'),
	(r'^hoopaloo/help/actions_log$', 'projectdjango.hoopaloo.help_views.help_actions_log'),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        #(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'E:/projectdjango/media/'}),
		#(r'^admin-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'E:/projectdjango/admin-media/'}),
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'C:\\Documents and Settings\\Mari\\workspaceVE\\projectdjango\\media\\'}),
		(r'^admin-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'C:\\Documents and Settings\\Mari\\workspaceVE\\projectdjango\\admin-media\\'}),
    )

