from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Organization
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from .form import RegisterationForm,LoginForm
def regOrgView(request):
    if request.user.is_authenticated:
        return redirect(reverse('list'))
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            p1=form.cleaned_data["password1"]
            p2=form.cleaned_data["password2"]
            email=form.cleaned_data['email']
            organization=form.cleaned_data["organization"]
            if User.objects.filter(username=username) or (p1!=p2):
                return redirect(reverse('register'))            
            
            user=User(username=username,email=email)
            user.set_password(p1)
            user.save()
            
            org=Organization(org_name=organization,num_of_users=0,head_user=user)
            org.save()
            return redirect(reverse('login'))     
            
    else:
        form =RegisterationForm()
        
    return render(request,'reg_form.html',{'form':form})

def loginView(request):
    
    if request.user.is_authenticated:
        return redirect(reverse('list'))
    if request.method == 'POST':
        form=LoginForm(request.POST)
        
        if form.is_valid():
            # print(form.cleaned_data)
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            
            user=authenticate(username=username,password=password)
            
            if user is not None:
                login(request,user)
                
                return redirect(reverse('list'))
            else:
                return redirect(reverse('login'))
            
    else:
        form=LoginForm()
    
    return render(request,'login.html',{'form':form})

def listView(request):
    
    return render(request,'list_user.html')


def logoutView(request):
    logout(request)
    
    
    # Redirect to a success page.
    
    return redirect(reverse('login'))