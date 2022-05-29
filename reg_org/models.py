from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Organization(models.Model):
    
    org_name=models.CharField(max_length=100,unique=True)
    
    num_of_users=models.IntegerField(default=0)
    
    head_user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    
    
    
