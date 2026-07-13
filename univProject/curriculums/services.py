from django.utils import timezone
from .models import Stage, Lesson, LessonAnswer, UserLessonProgress, MotivationMessage, SavedMaterial



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


def get_current_stage(user, major):
    progress = get_current_lesson(user, major)
    return progress.lesson.stage if progress else None


def count_stage_mates(user, major):
    stage = get_current_stage(user, major)
    if not stage:
        return 0
    return UserLessonProgress.objects.filter(
        lesson__stage=stage, status='in_progress'
    ).exclude(user=user).values('user').distinct().count()


def save_answer(user, question_id, content):
    LessonAnswer.objects.update_or_create(
        user=user, question_id=question_id,
        defaults={'content': content}
    )


def complete_lesson(user, lesson, reflection_content):
    progress, _ = UserLessonProgress.objects.get_or_create(user=user, lesson=lesson)
    progress.status = 'completed'
    progress.completed_at = timezone.now()
    progress.save()

    if reflection_content:
        MotivationMessage.objects.create(
            user=user, stage=lesson.stage, content=reflection_content
        )

    next_lesson = Lesson.objects.filter(
        stage=lesson.stage, order__gt=lesson.order
    ).order_by('order').first()

    if next_lesson:
        next_progress, _ = UserLessonProgress.objects.get_or_create(user=user, lesson=next_lesson)
        if next_progress.status == 'upcoming':
            next_progress.status = 'in_progress'
            next_progress.save()

    return next_lesson



def get_featured_motivation_message(major, stage):
    if not stage:
        return None
    return MotivationMessage.objects.filter(
        stage=stage
    ).select_related('user').order_by('-created_at').first()


def get_cheer_count(message):
    return message.cheers.count() if message else 0


def has_user_cheered(user, message):
    return message.cheers.filter(user=user).exists() if message else False



def get_roadmap(major):
    return Stage.objects.filter(major=major).prefetch_related('lessons')



def get_saved_materials(user, major):
    return SavedMaterial.objects.filter(
        user=user, material__major=major
    ).select_related('material')


def save_material(user, material_id):
    from .models import Material
    material = Material.objects.get(id=material_id)
    SavedMaterial.objects.get_or_create(user=user, material=material)


def unsave_material(user, material_id):
    SavedMaterial.objects.filter(user=user, material_id=material_id).delete()