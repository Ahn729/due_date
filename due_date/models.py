from datetime import date
from dateutil.relativedelta import relativedelta

from django.db.models import Model, DateField, CharField, IntegerField, ManyToManyField
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def validate_positive(value):
    if value <= 0:
        raise ValidationError(f"Value must be a positive integer.")

class ToDo(Model):
    """An action that is due to be performed on a regular basis."""

    EXEC_INTERVALS = (
        ('d', 'day'),
        ('w', 'week'),
        ('m', 'month'),
        ('y', 'year')
    )

    name = CharField(help_text="Name the action that has to be done",
                     max_length=100)
    first_exec_date = DateField(help_text="First time this action has to be executed",
                                blank=True, null=True)
    last_exec_date = DateField(help_text="Last time this action was executed",
                               blank=True, null=True)
    exec_frequency = IntegerField(help_text="How often do we need to do this?",
                                  default=1, validators=[validate_positive])
    exec_interval = CharField(help_text="Interval this has to be done.",
                              max_length=1,
                              choices=EXEC_INTERVALS,
                              default='w')
    users_responsible = ManyToManyField(to=User, help_text="Who is responsible for doing this?")

    class Meta:
        ordering = ['-first_exec_date']

    def get_absolute_url(self):
        return reverse('todo-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    def next_exec_date(self):
        if not self.last_exec_date:
            return self.first_exec_date
        if self.exec_interval == 'd':
            return self.last_exec_date + relativedelta(days=self.exec_frequency)
        if self.exec_interval == 'w':
            return self.last_exec_date + relativedelta(weeks=self.exec_frequency)
        if self.exec_interval == 'm':
            return self.last_exec_date + relativedelta(months=self.exec_frequency)
        if self.exec_interval == 'y':
            return self.last_exec_date + relativedelta(years=self.exec_frequency)
        return None

    def is_overdue(self):
        return self.next_exec_date() < date.today()
