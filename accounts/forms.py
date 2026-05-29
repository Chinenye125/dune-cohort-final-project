from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
  # Add an email field on top of the built-in username and password fields
   email = forms.EmailField(required=True)

class Meta:
  model = User
 # Include the built-in fields plus our custom email field
  fields = ['username', 'email', 'password1', 'password2']