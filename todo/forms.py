from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Task


class UserForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())

  class Meta:
    model = User
    fields = ('username', 'email', 'password')



class UserProfileForm(forms.ModelForm):
  class Meta:
    model = UserProfile 
    fields = ('backgroundimage',)


class TaskForm(forms.ModelForm):
  class Meta:
    model = Task
    fields = ('text',)
    widgets = {
        'text': forms.TextInput(
            attrs={'name': 'text', 'required': True, 'placeholder': 'Enter Task Here!', 'autofocus' : True}
        ),
    }
