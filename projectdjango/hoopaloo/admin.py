from projectdjango.hoopaloo.models import *
from django.contrib import admin

class ExerciseAdmin(admin.ModelAdmin):
	fields = ['name', 'description', 'available', 'owner']

admin.site.register(Exercise, ExerciseAdmin)
