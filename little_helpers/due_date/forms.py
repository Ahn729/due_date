from datetime import date

from django.forms import Form, DateField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class DoToDoForm(Form):
    done_date = DateField(help_text="When did you do this?")

    # Syntax: clean_{field name}
    def clean_done_date(self):
        '''Clean the renewal date field. Conditions:

        * Date not in the future
        '''
        # Getting data this way gets us the data "cleaned" and sanitized of
        # potentially unsafe input using the default validators, and converted
        # into the correct standard type for the data
        # (in this case a Python datetime.datetime object).
        data = self.cleaned_data['done_date']

        # Check if renewal date is in the past:
        if data > date.today():
            raise ValidationError(_("Invalid date: Date in the future."))

        # ALWAYS return cleaned data
        return data
