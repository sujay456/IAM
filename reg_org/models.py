from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Organization(models.Model):
    
    org_name=models.CharField(max_length=100,unique=True)
    
    num_of_users=models.IntegerField(default=0)
    
    head_user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    
    client_secret=models.UUIDField(default=uuid.uuid4,editable=False)
    
    def __str__(self):
        
        return f"{self.org_name} - {self.head_user.username}"
    
class IsRoot(models.Model):
    is_root=models.BooleanField(default=False)
    
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    
class PartOf(models.Model):
    
    org=models.ForeignKey(Organization, on_delete=models.CASCADE,null=True)
    
    emp=models.ForeignKey(User, on_delete=models.CASCADE,null=True) 
    
    EMPLOYEE='em'
    PROJECT_LEAD='pl'
    MANAGER='mr'
    
    choices=[
        (EMPLOYEE, 'EMPLOYEE'),
        (PROJECT_LEAD, 'PROJECT_LEAD'),
        (MANAGER, 'MANAGER')
    ]   
    
    prem=models.CharField(max_length=2,choices=choices,default=EMPLOYEE)
    
