from django.urls import path
from . import views



urlpatterns = [
  path('student_list', views.student_list, name='student_list'),
  path('del_student/<int:pk>', views.del_student, name='del_student'),
  path('profile/<slug:slug>', views.get_profile_from_student, name='student_profile'),
  path('message',views.message, name='message')
   
]