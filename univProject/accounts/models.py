from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=50, blank=True)
    STATUS_CHOICES = [
    ('survey', 'Survey'),
    ('exploring', 'Exploring'),
    ('selected', 'Selected'),
    ]
    exploration_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='survey')
    #최종 전공
    #selected_major = models.ForeignKey(flow.Major, on_delete=models.SET_NULL, null=True, blank=True, related_name='selected_users')
    #추천 전공 2개
    #recommended_major1 = models.ForeignKey(flow.Major, on_delete=models.SET_NULL, null=True, blank=True, related_name='recommended_as_first')
    #recommended_major2 = models.ForeignKey(flow.Major, on_delete=models.SET_NULL, null=True, blank=True, related_name='recommended_as_second')

    def __str__(self):
        return f"{self.user.username}'s profile"
=======

# Create your models here.
>>>>>>> dev
