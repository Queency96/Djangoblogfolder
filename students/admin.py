from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
  list_display = ['username', 'first_name', 'last_name', 'status', 'student_type', 'phone', 'email']

@admin.register(models.Student_Profile)
class StudentProfileAdmin(admin.ModelAdmin):
  list_display = ['student', 'date_join', 'DOB', 'address', 'rating']
  
@admin.register(models.Program)
class ProgramAdmin(admin.ModelAdmin):
  list_display = ['student', 'courses', 'grade']
  
@admin.register(models.Cohort_Group)
class CohortGroupAdmin(admin.ModelAdmin):
  list_display = ['name', 'date_join']
  
# admin.site.register(models.Student)
# admin.site.register( models.Program)
# admin.site.register(models.Student_Profile)
# admin.site.register(models.Cohort_Group)