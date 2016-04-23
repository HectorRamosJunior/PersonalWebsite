from django import forms
from django.contrib.auth.models import User
from .models import Score


class UserForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())

  class Meta:
    model = User
    fields = ('username', 'password')