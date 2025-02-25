from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    profile_image = models.ImageField(upload_to = "profile", blank = True)
    short_description = models.TextField(blank = True)
    
    def __str__(self):
        return f"{self.username}\t{self.date_joined}\t{self.profile_image}\t{self.short_description}\t{self.id}\t{self.email}"