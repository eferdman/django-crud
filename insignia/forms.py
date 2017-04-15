from django import forms
from sqlalchemy.types import *


class MyForm(forms.Form):
    MY_CHOICES = \
        (('String', 'Text'),
         ('Boolean', 'Checkbox'),
         ('BigInteger', 'SelectBox'),
         ('TEXT', 'Long Text'),
         ('Date', 'Date'),
         ('DECIMAL', 'Currency'),
         ('Float', 'Number'),
         ('DateTime', 'Timestamp'),
         ('VARCHAR(5)', 'Time'),
         ('BigInteger', 'Integer')
         );
    my_choice_field = forms.ChoiceField(choices=MY_CHOICES);
