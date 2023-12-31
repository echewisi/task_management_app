from django.urls import path
from .views import RegistrationView, ApiLoginView, ApiLogoutView, TaskListCreateView, TaskRetrieveUpdateDeleteView
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterPage, TaskReorder
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', TaskList.as_view(), name="tasks"),
    path('register/', RegisterPage.as_view(), name="register" ),
    path('login/', CustomLoginView.as_view(), name='custom-login'),    
    path("logout/", LogoutView.as_view(next_page= 'custom-login'), name='logout'),
    path("task/<int:pk>/", TaskDetail.as_view(), name="task"),
    path("create-task/", TaskCreate.as_view(), name="task-create"),
    path("update/<int:pk>/", TaskUpdate.as_view(), name= "task-update"),
    path('delete/<int:pk>/', TaskDelete.as_view(), name="task-delete"),
    path('task-redorder', TaskReorder.as_view(), name='task-reorder'),
    #API URLS HERE:
    path('api/register/', RegistrationView.as_view(), name='api-register'),
    path('api/login/', ApiLoginView.as_view(), name='api-login'),
    path('api/logout/', ApiLogoutView.as_view(), name='api-logout'),
    path('api/create/', TaskListCreateView.as_view(), name="api-create"),
    path('api/tasks/<int:pk>/', TaskRetrieveUpdateDeleteView.as_view(), name='api-task-detail'),
]
