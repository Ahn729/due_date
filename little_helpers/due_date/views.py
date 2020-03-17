from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView

from .models import ToDo

# Create your views here.

def index(request):
        return render(request, "index.html")


def todo_list_view(request):
    PAGINATE_BY = 5

    todo_list = sorted(ToDo.objects.all(), key=lambda x: x.next_exec_date())

    paginator = Paginator(todo_list, PAGINATE_BY)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_paginated = paginator.num_pages > 1

    context = {'todo_list': page_obj, 'page_obj': page_obj, 'is_paginated': is_paginated}
    return render(request, "due_date/todo_list.html", context=context)

class ToDoDetailView(DetailView):
    model = ToDo
