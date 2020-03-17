from django.contrib import admin

from .models import DueAction

class DueActionAdmin(admin.ModelAdmin):
    list_display = ('name', 'first_exec_date', 'last_exec_date',
                    'exec_frequency', 'exec_interval', 'next_exec_date',
                    'is_overdue')


# Register your models here.
admin.site.register(DueAction, DueActionAdmin)
