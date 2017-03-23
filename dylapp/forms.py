#from django import forms
from django.forms import ModelForm
from .models import Person

class NameForm(ModelForm):
	# last_name = forms.CharField(max_length=200)
	# first_name = forms.CharField(max_length=200)
	class Meta:
		model = Person
		fields = ['id', 'last_name', 'first_name']