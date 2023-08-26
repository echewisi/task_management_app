from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, TaskListCreateView, TaskRetrieveUpdateDeleteView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', TaskListCreateView.as_view(), name="create"),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDeleteView.as_view(), name='task-detail'),
]
