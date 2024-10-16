from django.urls import path
from . import views



urlpatterns = [
  path('student_list', views.student_list, name='student_list'),
   path('profile/<int:student_id>', views.get_profile_from_student, name='student_profile'),
]