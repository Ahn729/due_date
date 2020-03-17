from datetime import date
from dateutil.relativedelta import relativedelta

from django.db.models import Model, DateField, CharField, IntegerField

class DueAction(Model):
    """An action that is due to be performed on a regular basis."""

    EXEC_INTERVALS = (
        ('d', 'daily'),
        ('w', 'weekly'),
        ('m', 'monthly'),
        ('y', 'yearly')
    )

    name = CharField(help_text="Name the action that has to be done",
                     max_length=100)
    first_exec_date = DateField(help_text="First time this action has to be executed",
                                blank=True, null=True)
    last_exec_date = DateField(help_text="Last time this action was executed",
                               blank=True, null=True)
    exec_frequency = IntegerField(default=1)
    exec_interval = CharField(help_text="Interval this has to be done.",
                              max_length=1,
                              choices=EXEC_INTERVALS,
                              default='w')

    class Meta:
        ordering = ['-first_exec_date']

    def __str__(self):
        return self.name

    def next_exec_date(self):
        if not self.last_exec_date:
            return self.first_exec_date
        elif self.exec_interval == 'd':
            return self.last_exec_date + relativedelta(days=self.exec_frequency)
        elif self.exec_interval == 'w':
            return self.last_exec_date + relativedelta(weeks=self.exec_frequency)
        elif self.exec_interval == 'm':
            return self.last_exec_date + relativedelta(months=self.exec_frequency)
        elif self.exec_interval == 'y':
            return self.last_exec_date + relativedelta(years=self.exec_frequency)

    def is_overdue(self):
        return self.next_exec_date() < date.today()
