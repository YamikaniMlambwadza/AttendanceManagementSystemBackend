# instructors/serializers.py
from rest_framework import serializers
from .models import Instructor, Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'code']

class InstructorSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True, source='course_set')

    class Meta:
        model = Instructor
        fields = ['id', 'username', 'instructor_id', 'courses']
