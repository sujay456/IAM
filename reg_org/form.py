from django import forms
from django.contrib.auth.models import User

class RegisterationForm(forms.Form):
    
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Username'}))
    email = forms.EmailField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'email'}))
    organization = forms.CharField(label='Organization',max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Organization'}))
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

    password1.widget.attrs.update({'class': 'form-control'})
    password1.widget.attrs.update({'placeholder': 'Password'})
    
    password2.widget.attrs.update({'class': 'form-control'})
    password2.widget.attrs.update({'placeholder': 'confirm Password'})

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Username'}))
    password= forms.CharField(widget=forms.PasswordInput)
    
    password.widget.attrs.update({'class': 'form-control'})
    password.widget.attrs.update({'placeholder': 'Password'})
    

class EmployeeRegForm(forms.ModelForm):
    class Meta:
        model=User 
        fields=['username', 'email','password']
        

class EmployeeUpdForm(forms.Form):
    
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Username'}))
    email = forms.EmailField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'email'}))
    
    
    EMPLOYEE='em'
    PROJECT_LEAD='pl'
    MANAGER='mr'
    
    choices=[
        (EMPLOYEE, 'EMPLOYEE'),
        (PROJECT_LEAD, 'PROJECT_LEAD'),
        (MANAGER, 'MANAGER')
    ]   
    
    
    prem=forms.ChoiceField(choices=choices)
    
    