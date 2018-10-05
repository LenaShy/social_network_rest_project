from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email_hunter_json = models.TextField(null=True, blank=True)
    clearbit_json = models.TextField(null=True, blank=True)


