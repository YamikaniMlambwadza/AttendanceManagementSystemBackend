#      attendance_summary/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('fetch-attendance-summary/', views.fetch_attendance_summary, name='fetch_attendance_summary'),
]
