from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, TaskListCreateView, TaskRetrieveUpdateDeleteView
from .views import TaskLIst, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', TaskLIst.as_view(), name="tasks"),
    path('register/', RegisterPage.as_view(), name="register" ),
    path(r"^accounts/login/", CustomLoginView.as_view(), name= "login" ),
    path("logout/", LogoutView.as_view(next_page= 'login'), name='logout'),
    path("task/<int:pk>/", TaskDetail.as_view(), name="task"),
    path("create-task/", TaskCreate.as_view(), name="task-create"),
    path("update/<int:pk>/", TaskUpdate.as_view(), name= "task-update"),
    path('delete/<int:pk>/', TaskDelete.as_view(), name="task-delete"),
    #API URLS HERE:
    path('api/register/', RegistrationView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/create/', TaskListCreateView.as_view(), name="create"),
    path('api/tasks/<int:pk>/', TaskRetrieveUpdateDeleteView.as_view(), name='task-detail'),
]
