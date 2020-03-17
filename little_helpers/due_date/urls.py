from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('todos/', views.todo_list_view, name='todos'),
    path('todos/<int:pk>', views.ToDoDetailView.as_view(), name='todo-detail'),
]
