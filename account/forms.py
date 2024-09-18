from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import BorrowBooks



class UserRegistrationForm(UserCreationForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
    email=forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
    

    class Meta:
        model = User
        fields=['username','first_name','last_name','email']



class UserUpdateForm(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']   

class UserHistory(forms.ModelForm):
    
    class Meta:
        model=BorrowBooks
        fields='__all__'          
           