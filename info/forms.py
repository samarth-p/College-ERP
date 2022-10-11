from django import forms
from django.contrib.auth.models import User

class PasswordResetForm(forms.Form):
    email= forms.CharField(max_length=100)
