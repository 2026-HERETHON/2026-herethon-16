from .models import Lesson, UserLessonProgress


def get_major_progress(user, major):
    lessons = Lesson.objects.filter(stage__major=major, is_experiential=False)
    total = lessons.count()
    completed = UserLessonProgress.objects.filter(
        user=user, lesson__in=lessons, status='completed'
    ).count()
    return {'completed': completed, 'total': total}


def get_current_lesson(user, major):
    return UserLessonProgress.objects.filter(
        user=user, lesson__stage__major=major, status='in_progress'
    ).select_related('lesson').first()