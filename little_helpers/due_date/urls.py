from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('todos/', views.todo_list_view, name='todos'),
    path('todos/create', views.ToDoCreate.as_view(), name='todo-create'),
    path('todos/<int:pk>', views.todo_list_detail, name='todo-detail'),
    path('todos/<int:pk>/delete', views.ToDoDelete.as_view(), name='todo-delete'),
]
