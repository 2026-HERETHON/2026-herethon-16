from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Material
from curriculums.models import Bookmark


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
        from curriculums.models import Stage

        stages = Stage.objects.filter(major=major).order_by('order')

        sections = []
        for stage in stages:
            stage_materials = Material.objects.filter(
                stages=stage, is_active=True
            ).order_by('display_order')
            if stage_materials.exists():
                sections.append({
                    'stage': stage,
                    'materials': stage_materials,
                })
        context['sections'] = sections

    else:
        materials = Material.objects.filter(majors=major, is_active=True)
        if material_type != 'all':
            materials = materials.filter(material_type=material_type)
        context['materials'] = materials.order_by('display_order')

    return render(request, 'materials/material_list.html', context)