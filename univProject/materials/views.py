from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Material, Bookmark


@login_required
def material_list_view(request):
    major = request.user.profile.selectedMajor
    scope = request.GET.get('scope', 'stage')
    material_type = request.GET.get('type', 'all')

    bookmarked_ids = set(
        Bookmark.objects.filter(user=request.user).values_list('material_id', flat=True)
    )

    context = {
        'major': major,
        'bookmarked_ids': bookmarked_ids,
        'scope': scope,
        'material_type': material_type,
    }

    if scope == 'stage':

        from curriculums.models import Lesson

        lessons = Lesson.objects.filter(
            stage__major=major, is_experiential=False
        ).select_related('stage').order_by('stage__order', 'order')

        sections = []
        for lesson in lessons:
            lesson_materials = Material.objects.filter(
                lessons=lesson, is_active=True
            ).order_by('display_order')
            if lesson_materials.exists():
                sections.append({
                    'lesson': lesson,
                    'materials': lesson_materials,
                })
        context['sections'] = sections

    else:
        materials = Material.objects.filter(majors=major, is_active=True)
        if material_type != 'all':
            materials = materials.filter(material_type=material_type)
        context['materials'] = materials.order_by('display_order')

    return render(request, 'materials/material_list.html', context)


@login_required
def bookmarked_materials_view(request):
    major = request.user.profile.selectedMajor

    from curriculums.services import get_major_progress
    progress = get_major_progress(request.user, major)

    bookmarks = Bookmark.objects.filter(
        user=request.user, material__majors=major
    ).select_related('material')

    context = {'major': major, 'progress': progress, 'bookmarks': bookmarks}
    return render(request, 'materials/bookmarked_materials.html', context)


@login_required
def material_bookmark_toggle(request, material_id):
    if request.method != 'POST':
        return redirect('material_list')

    material = get_object_or_404(Material, id=material_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, material=material)
    if not created:
        bookmark.delete()

    next_url = request.POST.get('next') or 'material_list'
    return redirect(next_url)