# instructors/urls.py
from django.urls import path
from .views import LoginView, InstructorCoursesView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('course/', InstructorCoursesView.as_view(), name='course'),
 
]


