from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=50, blank=True)
    STATUS_CHOICES = [
    ('survey', 'Survey'),
    ('exploring', 'Exploring'),
    ('selected', 'Selected'),
    ]

    exploration_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='survey')
   
    def __str__(self):
        return f"{self.user.username}'s profile"

