from datetime import date

from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, DeleteView
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import DoToDoForm
from .models import ToDo
from .serializers import ToDoSerializer, DoToDoSerializer

@login_required
def index(request):
    num_todos = ToDo.objects.count()
    current_user_name = request.user.username
    num_own_todos = ToDo.objects.filter(users_responsible__username=current_user_name).count()
    # This will be slow if there are many objects (see below).
    num_todos_due = len([x for x in ToDo.objects.all() if x.next_exec_date() < date.today()])
    num_own_todos_due = len([
        x for x in ToDo.objects.filter(users_responsible__username=current_user_name).all()
        if x.next_exec_date() < date.today()
    ])

    context = {'num_todos': num_todos, 'num_todos_due': num_todos_due,
               'num_own_todos': num_own_todos, 'num_own_todos_due': num_own_todos_due}
    return render(request, "index.html", context)

@login_required
def todo_list_view(request):
    paginate_by = 5
    # Cannot use standard 'order_by' here as we're ordering by a Python Function
    # which cannot be translated into an SQL statement. As a result, we're
    # getting _all_ objects from the db. This may cause performance issues
    # if we're dealing with many items!
    todo_list = sorted(ToDo.objects.all(), key=lambda x: x.next_exec_date())

    paginator = Paginator(todo_list, paginate_by)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_paginated = paginator.num_pages > 1

    context = {'todo_list': page_obj, 'page_obj': page_obj, 'is_paginated': is_paginated}
    return render(request, "due_date/todo_list.html", context=context)

@login_required
def todo_list_detail(request, pk):
    """Gets a todo or updates last exec date"""
    todo = get_object_or_404(ToDo, pk=pk)

    if request.method == 'POST':
        # Create form instance bound to data from POST request
        form = DoToDoForm(request.POST)
        if form.is_valid():
            # Get sanitized form input
            todo.last_exec_date = form.cleaned_data['done_date']
            todo.save()

            return HttpResponseRedirect(todo.get_absolute_url())

    # If this is a GET request, prepare default form
    else:
        proposed_done_date = date.today()
        form = DoToDoForm(initial={'done_date': proposed_done_date})

    context = {
        'form': form,
        'todo': todo
    }

    return render(request, 'due_date/todo_detail.html', context=context)

# LoginRequiredMixin must go first
class ToDoCreate(LoginRequiredMixin, CreateView):
    model = ToDo
    fields = '__all__'
    success_url = reverse_lazy('todos')

    # you really shouldn't do this [validate] in form_valid at all. form_valid()
    # is not what it's for. The right place to do this is validate using clean()
    def form_valid(self, form):
        if not form.cleaned_data['first_exec_date'] and not form.cleaned_data['last_exec_date']:
            form.add_error(None, 'You must specify either first or last exec date')
            return self.form_invalid(form)
        return super().form_valid(form)

# LoginRequiredMixin must go first
class ToDoDelete(LoginRequiredMixin, DeleteView):
    model = ToDo
    success_url = reverse_lazy('todos')

###
# REST rest_framework views
###

class ToDoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows todos to be viewed or created.

    GET: Displays all ToDos
    POST: Creates new ToDo
    """
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]

# Default Permissions for API are defined in settings.py module
@api_view(['GET', 'PUT'])
def todo_detail(request, pk):
    """API endpoint to get single todo or update its last exec date

    GET: Displays single ToDo
    PUT: Updates last exec date
    """

    todo = get_object_or_404(ToDo, pk=pk)
    if request.method == 'GET':
        serializer = ToDoSerializer(todo)
        return Response(data=serializer.data)

    if request.method == 'PUT':
        serializer = DoToDoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(ToDoSerializer(todo).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
