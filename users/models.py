from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=20)
    address = models.TextField()
    
    def __str__(self):
        return self.username
