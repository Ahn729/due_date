from datetime import date

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

from .forms import DoToDoForm
from .models import ToDo

# Create your views here.

def index(request):
    return render(request, "index.html")


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

def todo_list_detail(request, pk):
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
