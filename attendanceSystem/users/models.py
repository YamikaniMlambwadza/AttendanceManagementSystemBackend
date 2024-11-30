from django.db import models
# instructors/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser

class Instructor(AbstractUser):
    instructor_id = models.CharField(max_length=10, unique=True)

    # Avoid conflicts by adding unique `related_name` values
    groups = models.ManyToManyField(
        'auth.Group',
        related_name="instructors_groups",  # Custom related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="instructors_permissions",  # Custom related_name
        blank=True
    )

    def __str__(self):
        return self.username
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)