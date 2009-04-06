# coding: utf-8

#Hoopaloo - Version 1.0 - 2008/2009
#Author: Mariana Romao do Nascimento - mariana@dsc.ufcg.edu.br

from django.conf import settings

TEST_DEFAULT_CODE = "import unittest \nfrom unittest import TestResult \n\n\nclass %s (unittest.TestCase): \n\n\tdef setUp(self):\n\t\t pass\n\n\n\tdef tearDown(self):\n\t\tpass"

UNDER_TEST_COMPLEMENT = "if __name__== '__main__':\n\tloader = unittest.TestLoader()\n\tloader.testMethodPrefix = 'undertest'\n\tsuite = loader.loadTestsFromTestCase(%s)\n\tr = TestResult()\n\tsuite.run(r)\n\tresult_file = open('result.txt', 'wb')\n\tresult_file.write(str(len(r.errors)))\n\tresult_file.write('\\n')\n\tresult_file.write(str(len(r.failures)))\n\tresult_file.write('\\n')\n\tresult_file.write(str(r.testsRun))\n\tresult_file.write('\\n')\n\tresult_file.write(str(r.wasSuccessful()))\n\tresult_file.write('\\n')\n\tfor e in r.errors:\n\t\tresult_file.write(e[1])\n\tfor f in r.failures:\n\t\tresult_file.write(f[1])\n\tresult_file.close()"

TEST_APPEND = "if __name__== '__main__':\n\tloader = unittest.TestLoader()\n\tsuite = loader.loadTestsFromTestCase(%s)\n\tr = TestResult()\n\tsuite.run(r)\n\tresult_file = open('result.txt', 'wb')\n\tresult_file.write(str(len(r.errors)))\n\tresult_file.write('\\n')\n\tresult_file.write(str(len(r.failures)))\n\tresult_file.write('\\n')\n\tresult_file.write(str(r.testsRun))\n\tresult_file.write('\\n')\n\tresult_file.write(str(r.wasSuccessful()))\n\tresult_file.write('\\n')\n\tfor e in r.errors:\n\t\tresult_file.write(e[1])\n\tfor f in r.failures:\n\t\tresult_file.write(f[1])\n\tresult_file.close()"

TEST_APPEND_STUDENT_FOLDER = "if __name__== '__main__':\n\tloader = unittest.TestLoader()\n\tsuite = loader.loadTestsFromTestCase(%s)\n\tr = TestResult()\n\tsuite.run(r)\n\tresult_file = open(%s + 'result.txt', 'wb')\n\tresult_file.write(str(len(r.errors)))\n\tresult_file.write('\\n')\n\tresult_file.write(str(len(r.failures)))\n\tresult_file.write('\\n')\n\tresult_file.write(str(r.testsRun))\n\tresult_file.write('\\n')\n\tresult_file.write(str(r.wasSuccessful()))\n\tresult_file.write('\\n')\n\tfor e in r.errors:\n\t\tresult_file.write(e[1])\n\tfor f in r.failures:\n\t\tresult_file.write(f[1])\n\tresult_file.close()"


INFINITE_LOOP_MSG = "The program entered in infinite loop."

EMAIL_SYSTEM = 'hoopaloo@dsc.ufcg.edu.br'
SMTP_SERVER = "anjinho.dsc.ufcg.edu.br" 
BACKUP_TEST_NAME = 'backup_test'

PASSWORD_EMAIL = 'Welcome to Hoopaloo,\n\nYou are registered in the system and your login is: %s and your password is %s.\nThanks,\nHoopaloo.'
FORGOT_PASSWORD_EMAIL = 'Hello %s,\nYou requested a new password. This password is %s and you must change it when access Hoopaloo system at the next time.\n\nThanks, Hoopaloo.'

SUBMISSION_WITHOUT_TEST_EMAIL_TO_STUDENT = "%s,\nYour program was submited sucessfully, but at the moment there are not tests registered.\nWhen tests will be added, your program will be executed and the results sent to you by email.\n\nDo not reply this message, it is generated automatically.\n\nThanks,\nHoopaloo"

SUBMISSION_WITHOUT_TEST_EMAIL_TO_TEACHER = "Teacher,\nThere are submissions to the exercise %s, but you do not register any test.\n\nDo not reply this message, it is generated automatically.\n\nThanks,\nHoopaloo."

RESULT_TEST_FILE = 'result.txt'

PERCENT_OF_TESTS = [100, 90, 70, 50, 30, 20, 10, 0]
PERCENT_OF_SCORE = [(10.0, 9.1), (9.0, 8.1), (8.0, 7.1), (7.0, 6.1), (6.0, 5.1), (5.0, 4.1), (4.0, 3.1), (3.0, 2.1), (2.0, 1.1), (1.0, 0.0)]

LOGIN_SUCESS = 'You are logged'
LOGOUT_SUCESS = 'You are unlogged'
UNDELIVERED_EXERCISES_MSG = 'You not submited the following exercises and the deadline for the submission is expired.'
#duvida na frase abaixo
DELIVERED_EXERCISES_MSG = 'You submit the following exercises. You can modify your submission if you want.'
AVAILABLE_EXERCISES_MSG = 'The following exercises are available for submission.'
UNDELIVERED_AVAILABLE_EXERCISES_MSG = 'You not submited the following exercises. You must verify the deadline for them.'

REALIZED_SUBMISSIONS = 'All submissions that you realized in Hoopaloo are listed bellow.'
TEACHER_VIEW_EXPLICATION = 'There are not registered students.'

PASSWORD_CHANGED_MSG = 'Your password was changed.'
PASSWORD_NOT_MATCHES = 'The two password fields did not match.'
INVALID_PASSWORD = 'The password is invalid.'

FORGOT_PASSWORD = 'Please check your email. If you did not receive any message, check your spam folder.'

ASSIGN_SUCESS = 'The assign students to assistant(s) was done sucessfully.'
ASSIGN_ERROR = 'You have not permission to assign students to assistants.'
REVIEW_ASSIGN = 'Review the assigns students to assistant(s) bellow. See usernames with attention.'

EXERCISE_ADD_SUCESS = 'The exercise was added sucessfully. If you want edit the default test to this exercise click on link "Exercises > List Tests" and edit it.'
EXERCISE_ADD_ERROR = 'Some error exists in your form.'
EXERCISE_ADD_ERROR_DATE = 'Review the date.'
EXERCISE_EXISTS = 'An exercise with the same name already exists.'
EXERCISE_UPDATED_SUCESSFULLY = 'The exercise was updated sucessfully.'
EXERCISE_UPDATE_AVAILABILITY = 'The exercise was updated sucessfully. Please, check the deadline to this exercise.'
EXERCISE_UPDATE_AVAILABILITY_ERROR = 'The execise was not updated. Change the dead line for this exercise before.'
EXERCISE_DELETED = 'The exercise was deleted sucessfully.' 
EXERCISE_UPDATE_FAIL = 'Select a date later than current date.'

ADD_NOTE_ERROR = "The score must be a integer or a decimal number (use '.' in this case)."
ADD_NOTE_ERROR_2 = 'The score must be between 0 and 10.'

EXECUTION_PASS = 'Your program passed in all tests (%d tests).'
EXECUTION_FAILED = 'Your program not passed in all tests. There are %d registered tests and you not passed in %d tests.'
#EXECUTION_FAILED = 'Your program passed in none tests.'
EXECUTION_LOOP = 'Your program entered in infinite loop.'
EXECUTION_AFTER = 'Your program was submited sucessfully, but at the moment there are not tests registered.\nWhen tests will be added, your program will be executed and the results sent to you by email.'

EXECUTION_SUCESS = 'The program of student %s passed in all tests of exercise %s. The link to see the code of program is http://dataccc.gmf.ufcg.edu.br/hoopaloo/submission/student%d/exercise/id=%d'

SUBMISSION_MSG = 'Do the upload of your program and select given exercise.'
SUBMISSION_ERROR = 'You must choose an exercise.'

ADD_COMMENT_SCORE_SUCESS = 'Comments/score are addedd sucessfully.'


TEST_UPDATE_SUCESS = 'The test was updated sucessfully and it will be executed automatically to all students.'
TEST_ADD_SUCESSFULLY = 'The test was added sucessfully.'
TEST_EXISTS = 'A test with the same name already exists.'
TEST_ADD_ERROR = 'Some error exists in your form.'
UNDER_TEST_ADD_SUCESSFULLY = 'The test under test was added sucessfullty. Choose the student submissions to execute.'

ASSISTANT_ADD_SUCESS = 'The assistants was added sucessfully.'
ASSISTANT_ADD_ERROR = 'The assistants bellow are not registered. Review usernames and emails for them.'
REVIEW_USERNAMES_AND_EMAILS = 'Rewiew usernames and emails.'

STUDENT_ADD_SUCESS = 'The students were added successfully.'
STUDENT_ADD_ERROR = 'The students bellow are not registered. Review usernames, studentID and emails for them.'

USER_DELETED = "The user was deleted successfully."
# PERMITIONS

EXERCISE_ADD_NOT_PERMISSION = 'You have not permission to add exercises.'
TEST_UPDATE_NOT_PERMISSION = 'You have not permission to change tests.'
TESTS_ADD_NOT_PERMISSION = 'You have not permission to add tests.'
EXERCISE_UPDATE_NOT_PERMISSION = 'You have not permission to change exercises.'
EXERCISE_SEE_NOT_PERMISSION = 'You have not permission to see exercise details.'
ASSISTANT_ADD_NOT_PERMISSION = 'You have not permission to add assistants.'
VIEW_USERS_NOT_PERMISSION = 'You have not permissions to see user details.'
DELETE_USERS_NOT_PERMISSION = 'You have not permission to delete users.'
ASSIGN_STUDENTS_NOT_PERMISSION = 'You have not permission to assign students to assistants.'
RESULT_SEE_NOT_PERMISSION = 'You have not permission to see submission data of students.'
TEST_SEE_NOT_PERMISSION = 'You have not permission to see the test details.'
INVALIDATE_TEST_NOT_PERMISSION = 'You have not permission to annul a test.'
TEACHER_VIEW_NOT_PERMISSION = 'You are not a teacher.'
ASSISTANT_VIEW_NOT_PERMISSION = 'You are not a assistant.'
SEE_ACTIONS_NOT_PERMISSION = 'You have not permission to see the system actions.'
STUDENT_ADD_NOT_PERMISSION = 'You have not permission to add students.'
SUBMISSION_NOT_PERMISSION = 'You have not permission to submit programs.'
SUBMISSION_SEE_NOT_PERMISSION = 'You have not permission to see submission details.'
DELETE_ASSOCIATION_NOT_PERMISSION = 'You have not permission to delete assigns between students and assistants.'

# ACTIONS #
LOG_LOGIN = "Realized login"
LOG_LOGOUT = "Realized logout"
LOG_CHANGE_PASSWORD = "Changed the password"
LOG_FORGOT_PASSWORD = "%s requested a new password to %s"
LOG_ASSIGN_STUDENTS = "Assign the assistant %s to students %s"
LOG_ADD_EXERCISE = "Registered new exercise: %s"
LOG_EDIT_EXERCISE = "Edited the exercise: %s"
LOG_EDIT_SUBMISSION = "Add coments or/and note to submission %d of student %s"
LOG_SUBMISSION = "Submit a solution to exercise %s"
LOG_ADD_TEST = "Registered new test: %s"
LOG_EDIT_TEST = "Edited the test: %s"
LOG_IVALIDATE_TEST = "Annuled a test: %s"
LOG_ADD_ASSISTANT = "Registered new assistant: %s"
LOG_ADD_STUDENT = "Registered new student: %s"
LOG_DELETE_EXERCISE = "Deleted the exercise %s"
LOG_DELETE_USER = "Deleted the user %s"
LOG_DELETE_ASSOCIATION = "Deleted the assign between the student %s and the assistant %s"