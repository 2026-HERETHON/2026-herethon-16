from django.conf import settings
from django.db import models


class Stage(models.Model):
    major = models.ForeignKey('search.Major', on_delete=models.CASCADE, related_name='stages')
    order = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['order']
        unique_together = ('major', 'order')

    def __str__(self):
        return f"{self.major} - {self.order}단계 {self.title}"


class Lesson(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='lessons')
    order = models.PositiveIntegerField()
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    result = models.CharField(max_length=100, blank=True)
    usage = models.CharField(max_length=150, blank=True)
    duration_minutes = models.PositiveIntegerField(default=10)
    is_experiential = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']
        unique_together = ('stage', 'order')

    def __str__(self):
        return f"{self.stage} - {self.order}차시 {self.title}"


class UserLessonProgress(models.Model):
    STATUS_CHOICES = [
        ('upcoming', '진행 예정'),
        ('in_progress', '진행중'),
        ('completed', '완료'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user} - {self.lesson} ({self.status})"


class MotivationMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='motivation_messages')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='motivation_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.content[:20]}"