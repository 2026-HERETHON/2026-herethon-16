from django.conf import settings
from django.db import models


class Stage(models.Model):
    STATUS_CHOICES = [
        ('in_progress', '진행중'),
        ('upcoming', '예정'),
        ('completed', '완료'),
    ]

    major = models.ForeignKey('search.Major', on_delete=models.CASCADE, related_name='stages')
    order = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    final_result = models.CharField(max_length=150, blank=True)  # "완성할 것: 콘텐츠 기획 미니 포트폴리오"
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')  # 로드맵 배지용 고정값

    class Meta:
        ordering = ['order']
        unique_together = ('major', 'order')

    def __str__(self):
        return f"{self.major} - {self.order}단계 {self.title}"

    @property
    def lesson_count(self):
        return self.lessons.count()

    @property
    def total_duration(self):
        return sum(self.lessons.values_list('duration_minutes', flat=True))


class Lesson(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='lessons')
    order = models.PositiveIntegerField()
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    result = models.CharField(max_length=100, blank=True)      # 결과물
    usage = models.CharField(max_length=150, blank=True)       # 활용
    duration_minutes = models.PositiveIntegerField(default=10)
    is_experiential = models.BooleanField(default=False)       # 진행도 계산에서 제외 여부

    class Meta:
        ordering = ['order']
        unique_together = ('stage', 'order')

    def __str__(self):
        return f"{self.stage} - {self.order}차시 {self.title}"


class LessonQuestion(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions')
    order = models.PositiveIntegerField()
    prompt = models.CharField(max_length=200)
    guide = models.CharField(max_length=200, blank=True)
    placeholder = models.TextField(blank=True)
    max_length = models.PositiveIntegerField(default=100)
    card_label = models.CharField(max_length=50)  # 완료 카드용 라벨

    class Meta:
        ordering = ['order']
        unique_together = ('lesson', 'order')

    def __str__(self):
        return f"{self.lesson} - Q{self.order}"


class LessonAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lesson_answers')
    question = models.ForeignKey(LessonQuestion, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user} - {self.question}"


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


class Cheer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cheers')
    message = models.ForeignKey(MotivationMessage, on_delete=models.CASCADE, related_name='cheers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'message')

    def __str__(self):
        return f"{self.user} → {self.message}"


class Material(models.Model):
    major = models.ForeignKey('search.Major', on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=150)
    duration_minutes = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SavedMaterial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_materials')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'material')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user} saved {self.material}"