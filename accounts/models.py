from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)  # override to make it unique
    date_of_birth = models.DateField(null=True, blank=True)

    GENDER_CHOICES = [
        ('female', 'Female'),
        ('male', 'Male'),
        ('custom', 'Custom'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)

    ACADEMIC_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('researcher', 'Researcher'),
        ('other', 'Other'),
    ]
    academic_status = models.CharField(max_length=20, choices=ACADEMIC_CHOICES, blank=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    banner = models.ImageField(upload_to='profile_banners/', null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
