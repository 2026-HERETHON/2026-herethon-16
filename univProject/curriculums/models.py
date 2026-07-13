from django.conf import settings
from django.db import models

#admin에서 데이터 넣을 때 헷갈릴 거 같아서 어떤 데이터 넣으면 되는지 주석 남겨놨습니다!

class Stage(models.Model):
    stage_id = models.CharField(max_length=20, unique=True)  # "M03-S1"
    major = models.ForeignKey('search.Major', on_delete=models.CASCADE, related_name='stages')
    order = models.PositiveIntegerField()  # stage_order
    title = models.CharField(max_length=16)  # stage_name, 명세서 글자수 제한
    summary = models.CharField(max_length=65, blank=True)  # stage_summary
    lesson_count = models.PositiveIntegerField(default=0)  # 명세서엔 고정값으로 옴
    estimated_minutes = models.PositiveIntegerField(default=0)
    deliverable_name = models.CharField(max_length=22, blank=True)  # "완성할 것"
    unlock_rule = models.CharField(max_length=50, blank=True)  # "전공 선택 완료" / "이전 단계 완료"

    class Meta:
        ordering = ['order']
        unique_together = ('major', 'order')

    def __str__(self):
        return f"{self.stage_id} {self.title}"


class Lesson(models.Model):
    lesson_id = models.CharField(max_length=20, unique=True)  # "M03-S1-L1"
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='lessons')
    order = models.PositiveIntegerField()  # lesson_order
    title = models.CharField(max_length=24)  # lesson_title
    card_summary = models.CharField(max_length=60, blank=True)  # 목록 카드용 요약
    detail_intro = models.TextField(blank=True)  # 상세 화면용 인트로
    core_activity = models.CharField(max_length=100, blank=True)
    duration_minutes = models.PositiveIntegerField(default=10)
    deliverable_name = models.CharField(max_length=100, blank=True)
    previous_lesson = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='next_lessons'
    )
    is_experiential = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']
        unique_together = ('stage', 'order')

    def __str__(self):
        return f"{self.lesson_id} {self.title}"


class LessonScreen(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='screen')

    page_title = models.CharField(max_length=50, blank=True)
    lesson_badge = models.CharField(max_length=20, blank=True)  # "1차시"
    lesson_intro = models.TextField(blank=True)
    deliverable_label = models.CharField(max_length=50, blank=True)
    usage_label = models.CharField(max_length=100, blank=True)
    detail_cta = models.CharField(max_length=18, blank=True)  # "수업 완료하기"
    autosave_text = models.CharField(max_length=50, blank=True)

    complete_title = models.CharField(max_length=50, blank=True)
    complete_subtitle = models.CharField(max_length=100, blank=True)
    result_section_title = models.CharField(max_length=50, blank=True)
    insight_title = models.CharField(max_length=50, blank=True)
    insight_body = models.TextField(blank=True)
    use_case_text = models.TextField(blank=True)

    reflection_title = models.CharField(max_length=20, blank=True)  # "한 줄 소감"
    reflection_help = models.CharField(max_length=100, blank=True)
    reflection_placeholder = models.CharField(max_length=100, blank=True)
    reflection_max_length = models.PositiveIntegerField(default=50)

    next_cta = models.CharField(max_length=18, blank=True)  # "2차시로 가기"
    next_lesson = models.ForeignKey(
        Lesson, null=True, blank=True, on_delete=models.SET_NULL, related_name='screen_next_refs'
    )

    def __str__(self):
        return f"Screen for {self.lesson}"


class LessonQuestion(models.Model):
    question_id = models.CharField(max_length=30, unique=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions')
    order = models.PositiveIntegerField()
    result_label = models.CharField(max_length=20)  # 완료 카드용 라벨: "상황"/"나의 행동"/"결과"
    question_text = models.CharField(max_length=32)
    help_text = models.CharField(max_length=52, blank=True)
    input_type = models.CharField(max_length=20, default='long_text')
    placeholder = models.CharField(max_length=80, blank=True)
    required = models.BooleanField(default=True)
    min_length = models.PositiveIntegerField(default=0)
    max_length = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ['order']
        unique_together = ('lesson', 'order')

    def __str__(self):
        return f"{self.lesson} - Q{self.order}"


class LessonAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lesson_answers')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(LessonQuestion, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user} - {self.question}"


class LessonProgress(models.Model):
    STATUS_CHOICES = [
        ('locked', '잠김'),
        ('available', '진행 예정'),
        ('in_progress', '진행중'),
        ('completed', '완료'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='locked')
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user} - {self.lesson} ({self.status})"


class LessonReflection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lesson_reflections')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='reflections')
    reflection_text = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user}: {self.reflection_text[:20]}"


class Material(models.Model):
    MATERIAL_TYPE_CHOICES = [
        ('lecture', '강의'),
        ('article', '아티클'),
        ('practice', '실습'),
        ('program', '프로그램'),
    ]
    PRICE_TYPE_CHOICES = [
        ('free', '무료'),
        ('paid', '유료'),
    ]

    material_id = models.CharField(max_length=20, unique=True)  # "R-M03-001"
    title = models.CharField(max_length=150)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPE_CHOICES)
    provider = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True)
    duration_text = models.CharField(max_length=30, blank=True)  # "약 12분", "4주 과정"
    price_type = models.CharField(max_length=10, choices=PRICE_TYPE_CHOICES, default='free')
    difficulty = models.CharField(max_length=20, blank=True)
    source_url = models.URLField(blank=True)
    thumbnail_asset_key = models.CharField(max_length=100, blank=True)

    majors = models.ManyToManyField('search.Major', related_name='materials', blank=True)
    stages = models.ManyToManyField(Stage, related_name='materials', blank=True)
    lessons = models.ManyToManyField(Lesson, related_name='materials', blank=True)

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