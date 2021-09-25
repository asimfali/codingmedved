from django import forms

from .models import *


class NameForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        exclude = ['']
