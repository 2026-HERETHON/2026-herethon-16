from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Exists, OuterRef

from .models import Post, PostLike, PostCheer, Comment, CommentLike
from curriculums.models import LessonReflection, ReflectionCheer


from django.utils import timezone
from datetime import timedelta
from curriculums.models import LessonReflection, LessonProgress, ReflectionCheer

@login_required
def post_list(request):
    major = request.user.profile.selectedMajor
    scope = request.GET.get('scope', 'major')

    if scope == 'all':
        posts = Post.objects.filter(board_scope='all').select_related('author', 'major').order_by('-created_at')
        category = request.GET.get('category')
        if category:
            posts = posts.filter(category=category)
    else:
        posts = Post.objects.filter(board_scope='major', major=major).select_related('author').order_by('-created_at')
        category = None

    context = {
        'posts': posts,
        'major': major,
        'scope': scope,
        'category': category,
    }

    if scope == 'major':
        current_progress = LessonProgress.objects.filter(
            user=request.user, status='in_progress'
        ).select_related('lesson__stage').first()
        stage = current_progress.lesson.stage if current_progress else None

        featured_reflection = None
        stage_mate_count = 0
        has_cheered = False

        if stage:
            featured_reflection = LessonReflection.objects.filter(
                lesson__stage=stage
            ).exclude(user=request.user).select_related('user__profile').first()
            stage_mate_count = LessonProgress.objects.filter(
                lesson__stage=stage, status__in=['in_progress', 'completed']
            ).exclude(user=request.user).values('user').distinct().count()
            if featured_reflection:
                has_cheered = featured_reflection.cheers.filter(user=request.user).exists()

        context.update({
            'stage': stage,
            'featured_reflection': featured_reflection,
            'stage_mate_count': stage_mate_count,
            'has_cheered': has_cheered,
        })
    else:
        one_week_ago = timezone.now() - timedelta(days=7)
        weekly_reflections = LessonReflection.objects.filter(
            created_at__gte=one_week_ago
        ).exclude(user=request.user).select_related('user__profile', 'lesson__stage__major')[:5]

        context['weekly_reflections'] = weekly_reflections

    return render(request, 'posts/post_list.html', context)

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    comments = post.comments.filter(parent=None).select_related('author').prefetch_related(
        'replies__author', 'replies__likes'
    ).annotate(
        like_count=Count('likes', distinct=True),
        has_liked=Exists(CommentLike.objects.filter(comment=OuterRef('pk'), user=request.user))
    ).order_by('created_at')

    for comment in comments:
        for reply in comment.replies.all():
            reply.like_count = reply.likes.count()
            reply.has_liked = reply.likes.filter(user=request.user).exists()

    has_liked = post.likes.filter(user=request.user).exists()
    has_cheered = post.cheers.filter(user=request.user).exists()

    context = {
        'post': post,
        'major': post.major,
        'comments': comments,
        'has_liked': has_liked,
        'has_cheered': has_cheered,
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    scope = request.GET.get('scope', 'major')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        board_scope = request.POST.get('board_scope', 'major')
        category = request.POST.get('category') or None

        post = Post.objects.create(
            author=request.user,
            major=request.user.profile.selectedMajor,
            board_scope=board_scope,
            category=category,
            title=title,
            content=content,
        )
        return redirect('post_detail', post_id=post.id)

    return render(request, 'posts/post_form.html', {'scope': scope})

@login_required
def post_like(request, post_id):
    if request.method != 'POST':
        return redirect('post_detail', post_id=post_id)

    post = get_object_or_404(Post, id=post_id)
    like, created = PostLike.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()

    return redirect('post_detail', post_id=post_id)


@login_required
def post_cheer(request, post_id):
    if request.method != 'POST':
        return redirect('post_detail', post_id=post_id)

    post = get_object_or_404(Post, id=post_id)
    PostCheer.objects.get_or_create(user=request.user, post=post)

    return redirect('post_detail', post_id=post_id)


@login_required
def comment_create(request, post_id):
    if request.method != 'POST':
        return redirect('post_detail', post_id=post_id)

    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content')
    parent_id = request.POST.get('parent_id')

    Comment.objects.create(
        post=post,
        author=request.user,
        content=content,
        parent_id=parent_id if parent_id else None,
    )
    return redirect('post_detail', post_id=post_id)


@login_required
def comment_like_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    like, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)
    if not created:
        like.delete()
    return redirect('post_detail', post_id=comment.post.id)


@login_required
def reflection_cheer_view(request, reflection_id):
    if request.method != 'POST':
        return redirect('post_list')

    reflection = get_object_or_404(LessonReflection, id=reflection_id)
    cheer, created = ReflectionCheer.objects.get_or_create(reflection=reflection, user=request.user)
    if not created:
        cheer.delete()

    next_url = request.POST.get('next') or 'post_list'
    return redirect(next_url)