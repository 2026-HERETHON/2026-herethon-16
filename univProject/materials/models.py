from django.conf import settings
from django.db import models


class Material(models.Model):
    MATERIAL_TYPE_CHOICES = [
        ('lecture', '강의'),
        ('article', '아티클'),
        ('practice', '실습'),
        ('program', '프로그램'),
        ('book', '도서'),
    ]
    PRICE_TYPE_CHOICES = [
        ('free', '무료'),
        ('paid', '유료'),
    ]

    material_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=150)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPE_CHOICES)
    provider = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True)
    duration_text = models.CharField(max_length=30, blank=True)
    price_type = models.CharField(max_length=10, choices=PRICE_TYPE_CHOICES, default='free')
    difficulty = models.CharField(max_length=20, blank=True)
    source_url = models.URLField(blank=True)
    thumbnail_asset_key = models.CharField(max_length=100, blank=True)

    majors = models.ManyToManyField('search.Major', related_name='materials', blank=True)
    stages = models.ManyToManyField('curriculums.Stage', related_name='materials', blank=True)
    lessons = models.ManyToManyField('curriculums.Lesson', related_name='materials', blank=True)

    recommendation_reason = models.CharField(max_length=100, blank=True)
    deadline = models.DateField(null=True, blank=True)
    last_checked_at = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'material')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} bookmarked {self.material}"