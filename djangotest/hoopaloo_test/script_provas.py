import os
from datetime import date
from django.contrib.auth.models import User
from django.conf import settings
from hoopaloo_test.models import Student, Exercise, Submission
from hoopaloo_test import configuration


def nada():
    path = "/home/mariana/www/prova1/"
    questao1 = "ProvaQuestao1"
    questao2 = "ProvaQuestao2"
    questao3 = "ProvaQuestao3"
    questa4 = "ProvaQuestao4"
    
    count_id = 00000001
    for root, dirs, files in os.walk(path, topdown=False):
        if (root != path) and (files):
            student_name = root.split("\\")[-1]
            email = student_name + '@hoopaloo_test.com'
            studentID = count_id + 10
            pwd = student_name
            u = User.objects.create_user(student_name, email, pwd)
            u.first_name = student_name
            u.is_active = True
            u.issuperuser = False
            u.is_staff = False
            u.user_permissions.add(37, 54, 55)
            u.save()
            st = Student().create_student(u, student_name, str(studentID), 'TurmaProva')
            st.save()
            
            q1 = Exercise.objects.get(name=questao1)
            q2 = Exercise.objects.get(name=questao2)
            q3 = Exercise.objects.get(name=questao3)
            q4 = Exercise.objects.get(name=questao4)
            filename1 = settings.MEDIA_ROOT + '\\' + student_name + '\\' + questao1 + '\\' + questao1 + '.py'
            filename2 = settings.MEDIA_ROOT + '\\' + student_name + '\\' + questao2 + '\\' + questao2 + '.py'
            filename3 = settings.MEDIA_ROOT + '\\' + student_name + '\\' + questao3 + '\\' + questao3 + '.py'
            filename4 = settings.MEDIA_ROOT + '\\' + student_name + '\\' + questao4 + '\\' + questao4 + '.py'
            
            for f in files:
                st_file = open(root + '\\' + f, 'r')
                contend = st_file.read()
                size = os.path.getsize(root + '\\' + f)
                if f == 'q1.py': 
                    other_file = open(filename1, 'wb')
                elif f == 'q2.py':
                    other_file = open(filename2, 'wb')
                elif f == 'q3.py':
                    other_file = open(filename3, 'wb')
                else:   
                    other_file = open(filename4, 'wb')
                other_file.write(contend)
                st_file.close()
                other_file.close()
                submission = Submission().create_submission(st, filename1, q1, size)
                submission.save()
            
                st.number_submissions += 1
                st.save()
                    
if __name__=="__main__":
    nada()
        