from xml.etree.ElementInclude import include
from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import SetPasswordForm  # type: ignore
from django.contrib.auth import get_user_model
class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1','new_password2']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','phone_no','photo','address','gender']

        

        
