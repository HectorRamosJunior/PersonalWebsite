from django import forms
from django.contrib.auth.models import User
from .models import TwotterProfile, Twoot


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(
                attrs={'name': 'username', 'required': True, 'placeholder': 'Username', 'autofocus' : True}
            ),
            'password': forms.PasswordInput(
                attrs={'name': 'password', 'required': True, 'placeholder': 'Password'}
            ),
        }


class TwotterProfileForm(forms.ModelForm):
  class Meta:
        model = TwotterProfile 
        fields = ('display_name', 'avatar_url') #,'background_url')
        widgets = {
            'display_name': forms.TextInput(
                attrs={'name': 'display_name', 'required': True, 'placeholder': 'Display Name'}
            ),
            'avatar_url': forms.URLInput(
                attrs={'name': 'avatar_url', 'placeholder': '(Optional) Avatar Image URL'}
            ),
#            'background_url': forms.URLInput(
#                attrs={'name': 'background_url', 'placeholder': '(Optional) Background Image URL'}
#            ),
        }


class SettingsForm(forms.ModelForm):
  class Meta:
        model = TwotterProfile 
        fields = ('display_name', 'description', 'location', 'birthday', 'avatar_url',)
        widgets = {
            'description': forms.Textarea(
                attrs={'style': 'width:100%;', 'rows':'3',}
            ),
        }

class TwootForm(forms.ModelForm):
  class Meta:
    model = Twoot
    fields = ('text',)
    widgets = {
        'text': forms.TextInput(
            attrs={'name': 'text', 'required': True, 'placeholder': '140 character max tweet', 'autofocus' : True}
        ),
    }