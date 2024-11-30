#   linkGoogle/models.py

from django.db import models

class VerifiedStudent(models.Model):
    registration_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    attended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.registration_number})"
