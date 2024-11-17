from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class User(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now) 
    first_name = models.CharField(max_length=255)  
    last_name = models.CharField(max_length=255)  
    email = models.EmailField(unique=True)  
    mobile_number = models.CharField(max_length=15, unique=True) 
    password = models.CharField(max_length=128)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    reference = models.CharField(max_length=255, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    notifi_count = models.IntegerField(default=0)

    # def save(self, *args, **kwargs):
    #     # Hash the password before saving
    #     if not self.pk:  # Check if the instance is being created (not updated)
    #         self.password = make_password(self.password)
    #     super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return self.first_name  # String representation of the model

    class Meta:
        db_table = 'user'  # Custom table name (optional)
        verbose_name = 'User'
        verbose_name_plural = 'Users'