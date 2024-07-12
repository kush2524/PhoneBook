from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Custom user model inheriting from AbstractUser
    phone_number = models.CharField(max_length=20)  # Phone number field
    email = models.EmailField(blank=True, null=True)  # Optional email field
    spam = models.IntegerField(default=0)  # Spam count field

class SpamNumber(models.Model):
    # Model to store spam numbers and their counts
    phone_number = models.CharField(max_length=20, unique=True)  # Phone number field (unique)
    spam_count = models.IntegerField(default=0)  # Spam count field

    def __str__(self):
        return self.phone_number  # String representation of the object (phone number)

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PhoneNumber(models.Model):
    # Model to store phone numbers
    number = models.CharField(max_length=20)  # Phone number field

    def __str__(self):
        return self.number  # String representation of the object (phone number)

class Name(models.Model):
    # Model to store names associated with phone numbers
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User associated with the name
    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE)  # Phone number associated with the name
    name = models.CharField(max_length=100)  # Name field

    def __str__(self):
        return self.name  # String representation of the object (name)
