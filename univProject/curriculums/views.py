from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Lesson, LessonAnswer, MotivationMessage, Cheer, SavedMaterial
from .services import (
    get_major_progress, get_current_lesson, get_current_stage, count_stage_mates,
    save_answer, complete_lesson,
    get_featured_motivation_message, get_cheer_count, has_user_cheered,
    get_roadmap, get_saved_materials, save_material, unsave_material,
)



@login_required
def my_major_view(request):
    major = request.user.profile.selectedMajor
    progress = get_major_progress(request.user, major)
    current = get_current_lesson(request.user, major)

    lessons = Lesson.objects.filter(stage__major=major).select_related('stage')

    context = {
        'major': major,
        'progress': progress,
        'current_lesson': current.lesson if current else None,
        'lessons': lessons,
    }
    return render(request, 'curriculums/my_major.html', context)


@login_required
def lesson_detail_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.questions.all()

    if request.method == 'POST':
        for question in questions:
            content = request.POST.get(f'question_{question.id}', '')
            save_answer(request.user, question.id, content)
        return redirect('lesson_complete', lesson_id=lesson.id)

    answers = {
        a.question_id: a.content
        for a in LessonAnswer.objects.filter(user=request.user, question__lesson=lesson)
    }

    context = {'lesson': lesson, 'questions': questions, 'answers': answers}
    return render(request, 'curriculums/lesson_detail.html', context)


@login_required
def lesson_complete_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    answers = LessonAnswer.objects.filter(
        user=request.user, question__lesson=lesson
    ).select_related('question')

    if request.method == 'POST':
        reflection = request.POST.get('reflection', '')
        next_lesson = complete_lesson(request.user, lesson, reflection)
        if next_lesson:
            return redirect('lesson_detail', lesson_id=next_lesson.id)
        return redirect('my_major')

    context = {'lesson': lesson, 'answers': answers}
    return render(request, 'curriculums/lesson_complete.html', context)



@login_required
def roadmap_view(request):
    major = request.user.profile.selectedMajor
    stages = get_roadmap(major)

    context = {'major': major, 'stages': stages}
    return render(request, 'curriculums/roadmap.html', context)



@login_required
def saved_materials_view(request):
    major = request.user.profile.selectedMajor
    saved = get_saved_materials(request.user, major)

    context = {'major': major, 'saved_materials': saved}
    return render(request, 'curriculums/saved_materials.html', context)


@login_required
def material_save_toggle(request, material_id):
    if request.method != 'POST':
        return redirect('saved_materials')

    if SavedMaterial.objects.filter(user=request.user, material_id=material_id).exists():
        unsave_material(request.user, material_id)
    else:
        save_material(request.user, material_id)

    return redirect('saved_materials')



@login_required
def together_view(request):
    major = request.user.profile.selectedMajor
    stage = get_current_stage(request.user, major)
    stage_mates_count = count_stage_mates(request.user, major)
    motivation_message = get_featured_motivation_message(major, stage)

    context = {
        'major': major,
        'stage': stage,
        'stage_mates_count': stage_mates_count,
        'motivation_message': motivation_message,
        'cheer_count': get_cheer_count(motivation_message),
        'has_cheered': has_user_cheered(request.user, motivation_message),
    }
    return render(request, 'curriculums/together.html', context)


@login_required
def cheer_message(request, message_id):
    if request.method != 'POST':
        return redirect('together')

    message = get_object_or_404(MotivationMessage, id=message_id)
    Cheer.objects.get_or_create(user=request.user, message=message)

    return redirect('together')