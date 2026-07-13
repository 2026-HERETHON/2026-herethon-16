from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Lesson, LessonAnswer, LessonProgress
from .services import (
    get_major_progress, get_current_lesson,
    save_lesson_answers, complete_lesson,
    get_lesson_reflections,
    get_roadmap, get_bookmarked_materials, toggle_bookmark,
)


@login_required
def my_major_view(request):
    major = request.user.profile.selectedMajor
    progress = get_major_progress(request.user, major)
    current = get_current_lesson(request.user, major)

    lessons = Lesson.objects.filter(stage__major=major).select_related('stage')

    progress_map = {
        p.lesson_id: p.status
        for p in LessonProgress.objects.filter(user=request.user, lesson__in=lessons)
    }
    for lesson in lessons:
        lesson.user_status = progress_map.get(lesson.id, 'locked')

    stage = current.lesson.stage if current else None
    reflections = get_lesson_reflections(stage, exclude_user=request.user)

    context = {
        'major': major,
        'progress': progress,
        'current_lesson': current.lesson if current else None,
        'lessons': lessons,
        'reflections': reflections,
    }
    return render(request, 'curriculums/my_major.html', context)

@login_required
def lesson_detail_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.questions.all()
    screen = getattr(lesson, 'screen', None)

    if request.method == 'POST':
        answers_dict = {
            str(q.id): request.POST.get(f'question_{q.id}', '') for q in questions
        }
        save_lesson_answers(request.user, lesson, answers_dict)
        return redirect('lesson_complete', lesson_id=lesson.id)

    saved_answers = {
        a.question_id: a.answer_text
        for a in LessonAnswer.objects.filter(user=request.user, lesson=lesson)
    }

    context = {
        'lesson': lesson,
        'screen': screen,
        'questions': questions,
        'answers': saved_answers,
    }
    return render(request, 'curriculums/lesson_detail.html', context)


@login_required
def lesson_complete_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    screen = getattr(lesson, 'screen', None)
    answers = LessonAnswer.objects.filter(
        user=request.user, lesson=lesson
    ).select_related('question')

    if request.method == 'POST':
        reflection = request.POST.get('reflection', '')
        next_lesson = complete_lesson(request.user, lesson, reflection)
        if next_lesson:
            return redirect('lesson_detail', lesson_id=next_lesson.id)
        return redirect('my_major')

    context = {'lesson': lesson, 'screen': screen, 'answers': answers}
    return render(request, 'curriculums/lesson_complete.html', context)


@login_required
def roadmap_view(request):
    major = request.user.profile.selectedMajor
    stages = get_roadmap(major)

    context = {'major': major, 'stages': stages}
    return render(request, 'curriculums/roadmap.html', context)


@login_required
def bookmarked_materials_view(request):
    major = request.user.profile.selectedMajor
    bookmarks = get_bookmarked_materials(request.user, major)

    context = {'major': major, 'bookmarks': bookmarks}
    return render(request, 'curriculums/bookmarked_materials.html', context)


@login_required
def material_bookmark_toggle(request, material_id):
    if request.method != 'POST':
        return redirect('bookmarked_materials')

    toggle_bookmark(request.user, material_id)
    return redirect('bookmarked_materials')