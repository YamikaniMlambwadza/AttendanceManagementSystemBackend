from django.urls import path
from .views import write_on_google_sheet

urlpatterns = [
    #  Other endpoints
    path('write-on-google-sheet/', write_on_google_sheet, name='write_on_google_sheet'),
]
