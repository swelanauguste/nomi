from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Add any additional fields if needed
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user.email
