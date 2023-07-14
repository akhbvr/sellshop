from django.db import models

from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    image = models.ImageField(upload_to='users/profile', null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
