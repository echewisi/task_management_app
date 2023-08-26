from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import TaskSerializer, ProfileSerializer, UserSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.contrib.auth import login, logout, authenticate
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from .models import Task, Profile
from rest_framework import status

class Viewtasks(viewsets.ModelViewSet):
    serializer_class= TaskSerializer
    queryset= Task.objects.all()
    permission_classes=(permissions.IsAuthenticated,)
    
class ProfileView(viewsets.ModelViewSet):
    serializer_class= ProfileSerializer
    queryset= Profile.objects.all()
    permission_classes= (permissions.IsAuthenticated,)
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TaskRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    
class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    @method_decorator(csrf_exempt)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            request.auth.delete()
            logout(request)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
# Create your views here.
