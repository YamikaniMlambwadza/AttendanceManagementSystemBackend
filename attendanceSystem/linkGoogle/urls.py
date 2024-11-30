from django.urls import path
from . import views
#
urlpatterns = [
    path('fetch-google-sheet/', views.fetch_sheet_data, name='fetch_google_sheet'),
]
