from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user     = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar   = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio      = models.TextField(blank=True, verbose_name='Giới thiệu')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Profile của {self.user.username}'