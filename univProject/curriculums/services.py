from django.utils import timezone
from .models import (
    Stage, Lesson, LessonAnswer, LessonProgress, LessonReflection,
    Bookmark, Material,
)


def get_major_progress(user, major):
    """전체 진행도: 체험학습 제외"""
    lessons = Lesson.objects.filter(stage__major=major, is_experiential=False)
    total = lessons.count()
    completed = LessonProgress.objects.filter(
        user=user, lesson__in=lessons, status='completed'
    ).count()
    return {'completed': completed, 'total': total}


def get_current_lesson(user, major):
    return LessonProgress.objects.filter(
        user=user, lesson__stage__major=major, status='in_progress'
    ).select_related('lesson').first()


def save_answer(user, question):
    def _save(content):
        LessonAnswer.objects.update_or_create(
            user=user, question=question,
            defaults={'lesson': question.lesson, 'answer_text': content}
        )
    return _save


def save_lesson_answers(user, lesson, answers_dict):
    """{question_id: content} 형태로 한번에 저장"""
    for question in lesson.questions.all():
        content = answers_dict.get(str(question.id), '')
        LessonAnswer.objects.update_or_create(
            user=user, question=question,
            defaults={'lesson': lesson, 'answer_text': content}
        )


def complete_lesson(user, lesson, reflection_text):
    progress, _ = LessonProgress.objects.get_or_create(user=user, lesson=lesson)
    progress.status = 'completed'
    progress.completed_at = timezone.now()
    progress.save()

    if reflection_text:
        LessonReflection.objects.update_or_create(
            user=user, lesson=lesson,
            defaults={'reflection_text': reflection_text}
        )

    next_lesson = Lesson.objects.filter(
        stage=lesson.stage, order__gt=lesson.order
    ).order_by('order').first()

    if not next_lesson:
        # 마지막 차시였다면 다음 단계의 첫 차시로
        next_stage = Stage.objects.filter(
            major=lesson.stage.major, order__gt=lesson.stage.order
        ).order_by('order').first()
        if next_stage:
            next_lesson = next_stage.lessons.order_by('order').first()

    if next_lesson:
        next_progress, _ = LessonProgress.objects.get_or_create(user=user, lesson=next_lesson)
        if next_progress.status in ('locked', 'available'):
            next_progress.status = 'in_progress'
            next_progress.save()

    return next_lesson


def get_lesson_reflections(stage, exclude_user=None, limit=5):
    if not stage:
        return LessonReflection.objects.none()

    qs = LessonReflection.objects.filter(lesson__stage=stage).select_related('user', 'lesson')
    if exclude_user:
        qs = qs.exclude(user=exclude_user)
    return qs.order_by('-created_at')[:limit]


def get_roadmap(major):
    """로드맵: 고정 데이터를 순서대로"""
    return Stage.objects.filter(major=major).prefetch_related('lessons')


def get_bookmarked_materials(user, major):
    return Bookmark.objects.filter(
        user=user, material__majors=major
    ).select_related('material')


def toggle_bookmark(user, material_id):
    material = Material.objects.get(id=material_id)
    bookmark, created = Bookmark.objects.get_or_create(user=user, material=material)
    if not created:
        bookmark.delete()
        return False
    return True