from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# You are right, even after you remove the JWT token it remains valid token for a period of time until it expires. JWT is stateless. So if you want to handle logout and to invalidate token you must need to keep a database or in memory cache to store the invalid(blacklisted) token. Then you need to add a new permission to check whether the token is blacklisted or not.

class BlackListedToken(models.Model):
    token = models.CharField(max_length=500)
    user = models.ForeignKey(User, related_name="token_user", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("token", "user")