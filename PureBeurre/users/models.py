from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=80)

