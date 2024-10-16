from django.urls import path
from .views import Bloghome, Post_list, about_us, contact_us



urlpatterns = [
    path('', Bloghome, name='home' ),
    path('about_us', about_us, name='about_us'),
    path('contact_us', contact_us, name='contact_us'),
    path('post_list', Post_list, name='post'),
]
 