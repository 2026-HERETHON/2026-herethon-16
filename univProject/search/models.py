from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Major(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    tag1 = models.CharField(max_length=30, blank=True)
    tag2 = models.CharField(max_length=30, blank=True)
    tag3 = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name
    
class Question(models.Model):
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order}. {self.title}"
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=200)
    reason = models.TextField(blank=True)

    def __str__(self):
        return self.text


class ChoiceScore(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="scores")
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.choice} - {self.major} ({self.score})"


class ScoreRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.major.name} ({self.score})"
    
class Experience(models.Model):
    major = models.ForeignKey(Major, on_delete=models.CASCADE, related_name="experiences")
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.title
    
class ExperienceQuestion(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name="questions")
    order = models.PositiveIntegerField()
    question = models.CharField(max_length=300)

    def __str__(self):
        return self.question