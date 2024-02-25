from django import forms
from .models import CustomUser
from allauth.account.forms import SignupForm
from allauth.account.models import EmailAddress
from allauth.account.adapter import get_adapter

class SignupUserForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='名字')
    last_name = forms.CharField(max_length=30, label='名前')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

class ProfileForm(forms.Form):
    full_name = forms.CharField(max_length=30, label='名前')


