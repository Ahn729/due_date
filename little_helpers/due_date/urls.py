from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'todos', views.ToDoViewSet, basename='api-todo')

urlpatterns = [
    path('', views.index, name='index'),
    path('todos/', views.todo_list_view, name='todos'),
    path('todos/create', views.ToDoCreate.as_view(), name='todo-create'),
    path('todos/<int:pk>', views.todo_list_detail, name='todo-detail'),
    path('todos/<int:pk>/delete', views.ToDoDelete.as_view(), name='todo-delete'),
    # REST framework
    path('api/', include(router.urls)),
    path('api/todos/<int:pk>', views.todo_detail),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
