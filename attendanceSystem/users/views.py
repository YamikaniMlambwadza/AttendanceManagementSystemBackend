from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import InstructorSerializer
from .models import Instructor

class LoginView(APIView):
    def post(self, request):
   
        print("Incoming Data:", request.data)
        instructor_id = request.data.get('instructor_id')
        password = request.data.get('password')

        # Check if both fields are provided
        if not instructor_id or not password:
            raise AuthenticationFailed('Instructor ID and Password are required')

        # Authenticate user using custom field (instructor_id instead of username)
        try:
            # Look up instructor by instructor_id and authenticate password
            instructor = Instructor.objects.get(instructor_id=instructor_id)
            if not instructor.check_password(password):
                raise AuthenticationFailed('Invalid credentials')

        except Instructor.DoesNotExist:
            raise AuthenticationFailed('Invalid credentials')

        # Create JWT tokens
        refresh = RefreshToken.for_user(instructor)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

'''from django.shortcuts import render

# instructors/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from .models import Instructor
from .serializers import InstructorSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    def post(self, request):
        print("Incoming Data:", request.data)
        instructor_id = request.data.get('instructor_id')
        password = request.data.get('password')

        instructor = authenticate(username=instructor_id, password=password)
        if not instructor:
            raise AuthenticationFailed('Invalid credentials')

        refresh = RefreshToken.for_user(instructor)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    '''

class InstructorCoursesView(APIView):
    def get(self, request):
        instructor = request.user
        serializer = InstructorSerializer(instructor)
        return Response(serializer.data)
