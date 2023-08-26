from django.shortcuts import render, redirect
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
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import PositionForm, UserCreationForm
from django.db import  transaction


class CustomLoginView(LoginView):  
    model=Task
    template_name: str= 'base/login.html'
    fields= ['username', 'password']
    redirect_authenticated_user= True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name= 'base/register.html'
    form_class= UserCreationForm
    redirect_authenticated_user=True
    success_url= reverse_lazy('tasks')

    def form_valid(self, form):
        user= form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

class TaskLIst(LoginRequiredMixin,ListView):
    #list view looks for object_list
    login_url='login/'
    model= Task
    context_object_name= "tasks" #by default this is "object_list"

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks']= context['tasks'].filter(user=self.request.user)
        context['count']= context['tasks'].filter(complete= False).count()
        search_input= self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']= context['tasks'].filter(title__icontains=search_input) #you can add a startswith to find items that begin with the particular letter passed in
        
        context['search-input']= search_input
        return context
    
class TaskDetail(LoginRequiredMixin, DetailView):
    #detailview looks for object
    model= Task
    context_object_name: str=  'task' #by default this is object
    template_name: str= "base/task.html" #by default list view finds a html template with named after the class it's assigned to. this function "template_name" is to change such

class TaskCreate(LoginRequiredMixin, CreateView): 
    model= Task
    template_name: str='base/task_form.html'
    fields= ['title', 'description', 'complete', 'reminder']
    success_url= reverse_lazy("tasks")

    def form_valid(self, form):
        form.instance.user= self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model= Task
    fields= ['title', 'description', 'complete', 'reminder']
    success_url= reverse_lazy("tasks")

class TaskDelete(LoginRequiredMixin, DeleteView):
    model=Task
    context_object_name: str= "task"
    success_url= reverse_lazy("tasks")
    def get_queryset(self):
        owner= self.request.user
        return self.model.objects.filter(user=owner)

class TaskReorder(View):
    def post(self, request):
        form= PositionForm(request.POST)
        
        if form.is_valid():
            positionList= form.cleaned_data["position"].split(',')
            with transaction.atomic():
                self.request.user.set_task_order(positionList)
        return redirect(reverse_lazy('tasks'))
    
#BELOW  ARE THE VIEWS FOR THE API
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

class ApiLoginView(APIView):
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

class ApiLogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            request.auth.delete()
            logout(request)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
# Create your views here.
