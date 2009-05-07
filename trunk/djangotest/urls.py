# coding: utf-8

#Hoopaloo - Version 1.0 - 2008/2009
#Author: Mariana Romao do Nascimento - mariana@dsc.ufcg.edu.br

from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
	
	(r'^hoopaloo_test/script$', 'djangotest.hoopaloo_test.views.script'),
	#AUTENTICATION_VIEWS
	(r'^hoopaloo_test/$', 'djangotest.hoopaloo_test.autentication_views.login'),
	(r'^hoopaloo_test/logout/$', 'djangotest.hoopaloo_test.autentication_views.logout'),
	(r'^hoopaloo_test/forgot_password/$', 'djangotest.hoopaloo_test.autentication_views.forgot_password'),
    (r'^admin/(.*)', admin.site.root),
	(r'^hoopaloo_test/login/$', 'djangotest.hoopaloo_test.autentication_views.login'),
	(r'^hoopaloo_test/.*/logout/$', 'djangotest.hoopaloo_test.autentication_views.logout'),
	(r'^hoopaloo_test/.*/password_change/$', 'djangotest.hoopaloo_test.autentication_views.change_password'),
	(r'^hoopaloo_test/change_password/$', 'djangotest.hoopaloo_test.autentication_views.change_password'),
	
	# USERS_VIEWS
	(r'^hoopaloo_test/register_student/$', 'djangotest.hoopaloo_test.users_views.register_student'),
	(r'^hoopaloo_test/register_assistant/$', 'djangotest.hoopaloo_test.users_views.register_assistant'),
	(r'^hoopaloo_test/delete_users/id=(?P<user_id>\d+)/$', 'djangotest.hoopaloo_test.users_views.delete_users'),
	(r'^hoopaloo_test/delete_user/id=(?P<user_id>\d+)/$', 'djangotest.hoopaloo_test.users_views.delete_user'),
	(r'^hoopaloo_test/users/$', 'djangotest.hoopaloo_test.users_views.users'),
	(r'^hoopaloo_test/assign_students/$', 'djangotest.hoopaloo_test.users_views.assign_students'),
	(r'^hoopaloo_test/assigns/$', 'djangotest.hoopaloo_test.users_views.assigns'),
	
	# GENERAL VIEWS
	(r'^hoopaloo_test/actions/$', 'djangotest.hoopaloo_test.views.actions'),
	(r'^hoopaloo_test/assistant_view/$', 'djangotest.hoopaloo_test.views.assistant_view'),
	(r'^hoopaloo_test/global_assistant_view/$', 'djangotest.hoopaloo_test.views.global_assistant_view'),
	(r'^hoopaloo_test/teacher_view/$', 'djangotest.hoopaloo_test.views.teacher_view'),
	(r'^hoopaloo_test/all_students/$', 'djangotest.hoopaloo_test.views.all_students'),
	(r'^hoopaloo_test/delivered_exercises/$', 'djangotest.hoopaloo_test.views.delivered_exercises'),
	(r'^hoopaloo_test/delivered_exercises/student/id=(?P<student_id>\d+)$', 'djangotest.hoopaloo_test.views.delivered_exercises_student'),
	(r'^hoopaloo_test/undelivered_exercises/$', 'djangotest.hoopaloo_test.views.undelivered_exercises'),
	(r'^hoopaloo_test/available_exercises/$', 'djangotest.hoopaloo_test.views.available_exercises'),
	(r'^hoopaloo_test/exercise/percentual/id=(?P<exercise_id>\d+)$', 'djangotest.hoopaloo_test.views.exercise_percentual'),
	(r'^hoopaloo_test/exercise/score_percentual/id=(?P<exercise_id>\d+)$', 'djangotest.hoopaloo_test.views.score_percentual'),
	(r'^hoopaloo_test/exercises/student/id=(?P<student_id>\d+)$', 'djangotest.hoopaloo_test.views.student_exercises'),
	(r'^hoopaloo_test/list_percentual(?P<percent>\d+)/id=(?P<id_exercise>\d+)$', 'djangotest.hoopaloo_test.views.list_percentual'),
	(r'^hoopaloo_test/list_score_percentual(?P<index>\d+)/id=(?P<id_exercise>\d+)$', 'djangotest.hoopaloo_test.views.list_score_percentual'),
	
	# EXERCISE_VIEWS
	(r'^hoopaloo_test/add_exercise/$', 'djangotest.hoopaloo_test.exercise_views.add_exercise'),
	(r'^hoopaloo_test/exercises/$', 'djangotest.hoopaloo_test.exercise_views.exercises'),
	(r'^hoopaloo_test/exercises/id=(?P<id_exercise>\d+)/$', 'djangotest.hoopaloo_test.exercise_views.exercises'),
	(r'^hoopaloo_test/change_exercise/id=(?P<exercise_id>\d+)/$', 'djangotest.hoopaloo_test.exercise_views.change_exercise'),
	(r'^hoopaloo_test/exercise/id=(?P<exercise_id>\d+)/$', 'djangotest.hoopaloo_test.exercise_views.exercise'),
	(r'^hoopaloo_test/change_exercise/id=(?P<exercise_id>\d+)$', 'djangotest.hoopaloo_test.exercise_views.change_exercise'),
	(r'^hoopaloo_test/delete_exercises/id=(?P<exercise_id>\d+)/$', 'djangotest.hoopaloo_test.exercise_views.delete_exercises'),
	(r'^hoopaloo_test/delete_exercise/id=(?P<exercise_id>\d+)/$', 'djangotest.hoopaloo_test.exercise_views.delete_exercise'),
	(r'^hoopaloo_test/change_availability_exercise/id=(?P<id_exercise>\d+)/$', 'djangotest.hoopaloo_test.exercise_views.change_availability_exercise'),
	(r'^hoopaloo_test/availability_exercise/id=(?P<id_exercise>\d+)/$', 'djangotest.hoopaloo_test.exercise_views.availability_exercise'),
	
	# TEST_VIEWS
	(r'^hoopaloo_test/tests/$', 'djangotest.hoopaloo_test.test_views.tests'),
	(r'^hoopaloo_test/change_test/id=(?P<test_id>\d+)/$', 'djangotest.hoopaloo_test.test_views.change_test'),
	(r'^hoopaloo_test/change_test/id=(?P<test_id>\d+)$', 'djangotest.hoopaloo_test.test_views.change_test'),
	(r'^hoopaloo_test/test_view/id=(?P<test_id>\d+)$', 'djangotest.hoopaloo_test.test_views.test_view'),
	(r'^hoopaloo_test/annul_test/id=(?P<test_id>\d+)/$', 'djangotest.hoopaloo_test.test_views.annul_test'),
	(r'^hoopaloo_test/under_test/id=(?P<test_id>\d+)/$', 'djangotest.hoopaloo_test.test_views.under_test'),
	(r'^hoopaloo_test/choose_submissions/id=(?P<exercise_id>\d+)/$', 'djangotest.hoopaloo_test.test_views.choose_submissions'),
	(r'^hoopaloo_test/undertest_view/id=(?P<undertest_id>\d+)$', 'djangotest.hoopaloo_test.test_views.undertest_view'),
	(r'^hoopaloo_test/save_under_test/id=(?P<undertest_id>\d+)/$', 'djangotest.hoopaloo_test.test_views.save_under_test'),
	(r'^hoopaloo_test/under_test_action/id=(?P<exercise_id>\d+)/$', 'djangotest.hoopaloo_test.test_views.under_test_action'),
	
	# SUBMISSION_VIEWS
	(r'^hoopaloo_test/submission/$', 'djangotest.hoopaloo_test.submission_views.submission'),
	(r'^hoopaloo_test/submission(?P<submission_id>\d+)/student(?P<student_id>\d+)/exercise/id=(?P<exercise_id>\d+)$', 'djangotest.hoopaloo_test.submission_views.view_exercise'),
	(r'^hoopaloo_test/submission(?P<submission_id>\d+)/student(?P<student_id>\d+)/exercise/id=(?P<exercise_id>\d+)/$', 'djangotest.hoopaloo_test.submission_views.view_exercise'),
	(r'^hoopaloo_test/submission(?P<submission_id>\d+)/student(?P<student_id>\d+)/$', 'djangotest.hoopaloo_test.submission_views.view_code'),
	(r'^hoopaloo_test/see_submissions/$', 'djangotest.hoopaloo_test.submission_views.see_submissions'),
	#(r'^hoopaloo_test/submissions/student(?P<student_id>\d+)/$', 'djangotest.hoopaloo_test.submission_views.submissions_student'),
	
	# HELPS
	(r'^hoopaloo_test/help$', 'djangotest.hoopaloo_test.help_views.help_index'),
	(r'^hoopaloo_test/help_student$', 'djangotest.hoopaloo_test.help_views.help_index_student'),
	(r'^hoopaloo_test/help/login$', 'djangotest.hoopaloo_test.help_views.help_login'),
	(r'^hoopaloo_test/help/register_student$', 'djangotest.hoopaloo_test.help_views.help_register_student'),
	(r'^hoopaloo_test/help/register_assistant$', 'djangotest.hoopaloo_test.help_views.help_register_assistant'),
	(r'^hoopaloo_test/help/register_exercise$', 'djangotest.hoopaloo_test.help_views.help_register_exercise'),
	(r'^hoopaloo_test/help/register_test$', 'djangotest.hoopaloo_test.help_views.help_register_test'),
	(r'^hoopaloo_test/help/assign$', 'djangotest.hoopaloo_test.help_views.help_assign'),
	(r'^hoopaloo_test/help/change_password$', 'djangotest.hoopaloo_test.help_views.help_change_password'),
	(r'^hoopaloo_test/help/forgot_password$', 'djangotest.hoopaloo_test.help_views.help_forgot_password'),
	(r'^hoopaloo_test/help/edit_exercise$', 'djangotest.hoopaloo_test.help_views.help_edit_exercise'),
	(r'^hoopaloo_test/help/edit_test$', 'djangotest.hoopaloo_test.help_views.help_edit_test'),
	(r'^hoopaloo_test/help/list_exercises$', 'djangotest.hoopaloo_test.help_views.help_list_exercises'),
	(r'^hoopaloo_test/help/list_tests$', 'djangotest.hoopaloo_test.help_views.help_list_tests'),
	(r'^hoopaloo_test/help/exercise_view$', 'djangotest.hoopaloo_test.help_views.help_exercise_view'),
	(r'^hoopaloo_test/help/test_view$', 'djangotest.hoopaloo_test.help_views.help_test_view'),
	(r'^hoopaloo_test/help/students_view$', 'djangotest.hoopaloo_test.help_views.help_students_view'),
	(r'^hoopaloo_test/help/exercises_student$', 'djangotest.hoopaloo_test.help_views.help_exercises_student'),
	(r'^hoopaloo_test/help/submission$', 'djangotest.hoopaloo_test.help_views.help_submission'),
	(r'^hoopaloo_test/help/submission_view$', 'djangotest.hoopaloo_test.help_views.help_submission_view'),
	(r'^hoopaloo_test/help/student_initial_page$', 'djangotest.hoopaloo_test.help_views.help_student_initial_page'),
	(r'^hoopaloo_test/help/assistant_initial_page$', 'djangotest.hoopaloo_test.help_views.help_assistant_initial_page'),
	(r'^hoopaloo_test/help/test_percentage$', 'djangotest.hoopaloo_test.help_views.help_test_percentage'),
	(r'^hoopaloo_test/help/note_percentual$', 'djangotest.hoopaloo_test.help_views.help_note_percentual'),
	(r'^hoopaloo_test/help/user_details$', 'djangotest.hoopaloo_test.help_views.help_user_details'),
	(r'^hoopaloo_test/help/actions_log$', 'djangotest.hoopaloo_test.help_views.help_actions_log'),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'E:/djangotest/media/'}),
		(r'^admin-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'E:/djangotest/admin-media/'}),
		#(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'C:\\Documents and Settings\\Mari\\workspaceVE\\djangotest\\media\\'}),
		#(r'^admin-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'C:\\Documents and Settings\\Mari\\workspaceVE\\djangotest\\admin-media\\'}),
    )

