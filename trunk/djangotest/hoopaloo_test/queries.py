from django.contrib.auth.models import User

	
# SUBMISSIONS
def get_submissions(exercise_id, student_id):
	"""Return all submissions of a student for an exercise."""
	from hoopaloo_test.models import Submission
	return Submission.objects.filter(id_exercise=exercise_id, id_student=student_id)

def get_ordered_submissions(exercise_id, student_id):
	"""Return all submissions of a student for an exercise in reverse order by date."""
	return get_submissions(exercise_id, student_id).order_by('date').reverse()
	
def get_student_submissions(student_id):
	"""Return all submissions of a student."""
	from hoopaloo_test.models import Submission
	return Submission.objects.filter(id_student=student_id)

def get_submission(submission_id):
	"""Return the submission represented by submission_id"""
	from hoopaloo_test.models import Submission
	return Submission.objects.get(pk=submission_id)
	
def get_ordered_student_submissions(student_id):
	"""Return all submissions of a student in reverse order by date."""
	return get_student_submissions(student_id).order_by('date').reverse()
	
def get_number_student_submissions(exercise_id, student_id):
	"""Return the number of submissions of a student for an exercise."""
	return get_submissions(exercise_id, student_id).count()
	
def get_last_submission(exercise_id, student_id):
	"""Return the last submission os a student for an exercise."""
	try:
		return get_ordered_submissions(exercise_id, student_id)[0]
	except:
		return None

def get_exercise_submissions(exercise_id):
	"""Return all submissions to an exercise."""
	from hoopaloo_test.models import Submission
	return Submission.objects.filter(id_exercise=exercise_id)
	
def get_number_total_student_submissions(student_id):
	"""Return the number of submissions of a student."""
	return get_student_submissions(student_id).count()

def get_all_submissions():
	from hoopaloo_test.models import Submission
	return Submission.objects.all()

def get_all_last_submissions(exercise_id):
	from hoopaloo_test.models import Student
	students = Student.objects.all()
	results = []
	for st in students:
		last_submission = get_last_submission(exercise_id, st.id)
		results.append(last_submission)
	return results
# EXERCISES
def get_all_exercises():
	"""Return all exercises."""
	from hoopaloo_test.models import Exercise
	return Exercise.objects.all()
	
def get_number_exercises():
	"""Return the number of exercises."""
	return get_all_exercises().count()
	
def get_exercise(exercise_id):
	"""Return the exercise represented by exercise_id."""
	from hoopaloo_test.models import Exercise
	return Exercise.objects.get(pk=exercise_id)

def get_all_exercises_ordered():
	"""Return all exercises in reverse order by date finish."""
	return get_all_exercises().order_by('date_finish').reverse()
	
def get_available_exercises():
	"""Return all available exercises."""
	from hoopaloo_test.models import Exercise
	return Exercise.objects.filter(available=True)

def get_ordered_available_exercises():
	"""Return available exercises ordered by date finish."""
	return get_available_exercises().order_by('date_finish')
	
def get_reverse_ordered_available_exercises():
	"""Return available exercises in reverse order by date finish."""
	return get_ordered_available_exercises().reverse()
	
def get_available_exercises_ordered_by_name():
	"""Return available exercises ordered by name."""
	return get_available_exercises().order_by('name')
	
def get_unavailable_exercises():
	"""Return unavailable exercise."""
	from hoopaloo_test.models import Exercise
	return Exercise.objects.filter(available=False)
	
def get_ordered_unavailable_exercises():
	"""Return unavailable exercises ordered by date finish."""
	return get_unavailable_exercises().order_by('date_finish')
	
def get_number_available_exercises():
	"""Return the number of available exercises."""
	return get_available_exercises().count()
	
def get_number_unavailable_exercises():
	"""Return the number of unavailable exercises."""
	return get_unavailable_exercises().count()
	
def get_number_exercises():
	"""Return the number of exercises."""
	return get_all_exercises().count()
	
def get_exercise_from_name(name_exercise):
	"""Return an exercise from its name."""
	from hoopaloo_test.models import Exercise
	return Exercise.objects.get(name=name_exercise)
	
def get_solved_exercises(student_id):
	"""Return all exercises solved by a student."""
	exercises = get_unavailable_exercises()
	result = []
	for ex in exercises:
		last_submission = get_last_submission(ex.id, student_id)
		if last_submission.veredict == 'Pass':
			result.append(ex)
	return result
		
def get_number_solved_exercises(student_id):
	"""Return the number of exercises solved by a student."""
	return get_solved_exercises(student_id).count()

def get_unsolved_exercises(student_id):
	"""Return all exercises unsolved by a student."""
	exercises = get_unavailable_exercises()
	result = []
	for ex in exercises:
		last_submission = get_last_submission(ex.id, student_id)
		if last_submission.veredict == 'Fail':
			result.append(ex)
	return result
		
def get_number_unsolved_exercises(student_id):
	"""Return the number of exercises unsolved by a student."""
	return get_unsolved_exercises(student_id).count()
	
def get_undelivered_exercises(student_id):
	"""Return all undelivered exercises of a student."""
	exercises = get_unavailable_exercises()
	result = []
	for ex in exercises:
		try:
			last_submission = get_last_submission(ex.id, student_id)
		except:
			result.append(ex)
	return result
		
def get_number_undelivered_exercises(student_id):
	"""Return the number of undelivered exercises of a student."""
	return len(get_undelivered_exercises(student_id))
	
	
# STUDENTS
def get_class_students(class_id):
	"""Return all students of a class."""
	from hoopaloo_test.models import Student
	return Student.objects.filter(student_class=class_id)
	
def get_ordered_class_student(class_id):
	"""Return all students of a class ordered by username."""
	return get_class_students(class_id).order_by('username')

def get_all_students():
	"""Return all students."""
	from hoopaloo_test.models import Student
	return Student.objects.all()

def get_all_students_ordered():
	"""Return students ordered by username."""
	return get_all_students().order_by('username')
	
def get_assistant_students(assistant_id):
	"""Return all students assisted by an assistant."""
	from hoopaloo_test.models import Student
	return Student.objects.filter(assistant=assistant_id)
	
def get_ordered_assistant_students(assistant_id):
	"""Return all students assisted by an assistant orederd by username."""
	return get_assistant_students(assistant_id).order_by('username')

def get_student(student_id):
	"""Return a student represented by student_id."""
	from hoopaloo_test.models import Student
	return Student.objects.get(pk=student_id)
	
def get_student_from_user_id(user_id):
	"""Return a student from hers/his user id."""
	from hoopaloo_test.models import Student
	return Student.objects.get(user=user_id)

def get_student_from_username(username_student):
	"""Return a student from hers/his username."""
	from hoopaloo_test.models import Student
	return Student.objects.get(username=username_student)
	
def get_students_that_solved(exercise_id):
	"""Return all students that solved an exercise."""
	students = get_all_students()
	result = []
	for st in students:
		last_submission = get_last_submission(exercise_id, st.id)
		try:
			if last_submission.veredict == 'Pass':
				result.append(st)
		except:
			pass
	return result

def number_students_that_solved(exercise_id):
	"""Return the number of students that solved an exercise."""
	return len(get_students_that_solved(exercise_id))
	
def get_students_that_submit(exercise_id):
	students = get_all_students()
	result = []
	for st in students:
		try:
			last_submission = get_last_submission(exercise_id, st.id)
			result.append(st)
		except:
			pass
	return students
		
# ASSISTANTS
def get_all_assistants():
	"""Return all assistants."""
	from hoopaloo_test.models import Assistant
	return Assistant.objects.all()
	
def get_all_assistants_ordered():
	"""Return all assistants ordered by username."""
	return get_all_assistants().order_by('username')
	
def get_assistant_from_user_id(user_id):
	"""Return an assistant from his/hers user id."""
	from hoopaloo_test.models import Assistant
	return Assistant.objects.get(user=user_id)
	
def get_assistant_from_username(username_assistant):
	"""Return an assistant from his/hers username."""
	from hoopaloo_test.models import Assistant
	return Assistant.objects.get(username=username_assistant)
	
# USERS
def get_user(user_id):
	"""Return an user represented by user_id."""
	return User.objects.get(pk=user_id)
	
def get_user_from_email(user_email):
	"""Return an user from his/hers email."""
	return User.objects.get(email=user_email)
	
def get_user_from_username(u):
	"""Return an user from his/hers username."""
	return User.objects.get(username=u)

# TESTS AND UNDER_TESTS
def get_consolidated_test(exercise_id):
	"""Return a conslidated test of an exercise."""
	from hoopaloo_test.models import Test
	return Test.objects.get(exercise=exercise_id)
	
def get_test(test_id):
	"""Return the test represented by test_id."""
	from hoopaloo_test.models import Test
	return Test.objects.get(pk=test_id)
	
def get_all_tests():
	"""Return all tests."""
	from hoopaloo_test.models import Test
	return Test.objects.all()

def get_under_test(exercise_id):
	from hoopaloo_test.models import UnderTest
	return UnderTest.objects.get(exercise=exercise_id)
	
def get_under_test2(undertest_id):
	from hoopaloo_test.models import UnderTest
	return UnderTest.objects.get(pk=undertest_id)
	
def get_user_undertest(user_id):
	from hoopaloo_test.models import UnderTest
	return UnderTest.objects.filter(owner=user_id)
	
#CLASSES
def get_classes(user):
	"""Return all classes."""
	from hoopaloo_test.models import Class
	return Class.objects.filter(teacher=user)

def get_class_from_name(class_name):
	"""Return a class from name."""
	from hoopaloo_test.models import Class
	return Class.objects.get(name=class_name)
	
def get_class(class_id):
	"""Return the class represented by class_id."""
	from hoopaloo_test.models import Class
	return Class.objects.get(pk=class_id)
	
# EXECUTIONS
def get_ordered_executions(submission_id):
	"""Return all executions of a submission in reverse order by date."""
	from hoopaloo_test.models import Execution
	return Execution.objects.filter(id_submission=submission_id).order_by('date').reverse()

def get_last_execution(submission_id):
	"""Return the last execution of a submission."""
	return get_ordered_executions(submission_id)[0]
	
	
# ACTIONS LOG
def get_last_100_actions():
	"""Return the last 100 action realized in the hoopaloo_test."""
	from hoopaloo_test.models import Actions_log
	return Actions_log.objects.all().order_by('date').reverse()[:100]