from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services import get_major_progress, get_current_lesson
from .models import Lesson


@login_required
def my_major_view(request):
    major = request.user.profile.selectedMajor

    progress = get_major_progress(request.user, major)
    current = get_current_lesson(request.user, major)

    lessons = Lesson.objects.filter(
        stage__major=major
    ).select_related('stage')

    context = {
        'major': major,
        'progress': progress,
        'current_lesson': current.lesson if current else None,
        'lessons': lessons,
    }
    return render(request, 'curriculum/my_major.html', context)