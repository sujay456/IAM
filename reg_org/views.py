from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Organization,IsRoot,PartOf
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
from .form import RegisterationForm,LoginForm,EmployeeRegForm,EmployeeUpdForm

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from django.contrib import messages
import uuid

def regOrgView(request):
    if request.user.is_authenticated:
        messages.error(request,"You are already logged in")
        return redirect(reverse('list'))
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            p1=form.cleaned_data["password1"]
            p2=form.cleaned_data["password2"]
            email=form.cleaned_data['email']
            organization=form.cleaned_data["organization"]
            if User.objects.filter(username=username) or (p1!=p2) or Organization.objects.filter(org_name=organization):
                
                if p1!=p2:
                    messages.error(request,'Passwords do not match')
                else:
                    messages.error(request,'Either organization or username is registered already')
                return redirect(reverse('register'))            
            
            user=User(username=username,email=email)
            user.set_password(p1)
            user.save()
            client_secret=uuid.uuid4()
            org=Organization(org_name=organization,num_of_users=0,head_user=user,client_secret=client_secret)
            org.save()
            
            IsRoot.objects.create(is_root=True,user=user)
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
                isroot=IsRoot.objects.get(user=user)
                
                if isroot.is_root==False:
                    
                    messages.error(request,"Invalid root credentials")
                    
                    return redirect(reverse('login'))
                login(request,user)
                messages.success(request,"Logged in successfully")
                return redirect(reverse('list'))
            else:
                messages.error(request,"Invalid credentials provided")
                return redirect(reverse('login'))
            
    else:
        form=LoginForm()
    
    return render(request,'login.html',{'form':form})

@login_required
def listView(request):
    
    try:
        org=Organization.objects.get(head_user=request.user)
        
        if request.method =='POST':
            form=EmployeeRegForm(request.POST)
            
            if form.is_valid():
                
                emp=form.save(commit=False)

                emp.set_password(form.cleaned_data['password'])
                emp.save()
                
                IsRoot.objects.create(is_root=False,user=emp)
                org.num_of_users+=1;
                org.save()
                
                PartOf.objects.create(org=org,emp=emp)
        else:
            form=EmployeeRegForm()
                
        all_emps=PartOf.objects.filter(org=org)
        print(org.client_secret)
        return render(request,'list_user.html',{'form':form,'num_of_users':org.num_of_users,'emps':all_emps,'client_secret':org.client_secret})
    
    except ObjectDoesNotExist:
        return render(request,'error.html',{'error':'data not found'})
    

@login_required
def empDetails(request,pk):
    
    try:
        user=User.objects.get(pk=pk)
        emp=PartOf.objects.get(emp=user)

        if request.method == 'POST':
            form=EmployeeUpdForm(request.POST)
            
            if form.is_valid():
                username=form.cleaned_data['username']
                email=form.cleaned_data['email']
                prem=form.cleaned_data['prem']
                
                user.username=username
                user.email=email
                user.save()
                
                emp.prem=prem
                
                emp.save()            
                messages.success(request,"changes updated successfully")

        form=EmployeeUpdForm({'username':user.username,'email':user.email,'prem':emp.prem})    
        
        return render(request,'empDetail.html',{'name':emp.emp.username,'org':emp.org.org_name,'prem_level':emp.prem,'form':form})
    except IntegrityError as e:
        return render(request,'error.html',{'error':'Cannot update'})
def logoutView(request):
    logout(request)
    
    messages.success(request,"Logged out successfully")
    # Redirect to a success page.
    
    return redirect(reverse('login'))