from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Post, PostLike, PostCheer, Comment


@login_required
@login_required
def post_list(request):
    major = request.user.profile.selectedMajor
    scope = request.GET.get('scope', 'major')  

    if scope == 'all':
        posts = Post.objects.select_related('author', 'major').order_by('-created_at')
    else:
        posts = Post.objects.filter(major=major).select_related('author').order_by('-created_at')

    context = {
        'posts': posts,
        'major': major,
        'scope': scope,
    }
    return render(request, 'posts/post_list.html', context)


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(parent=None).select_related('author').order_by('created_at')

    has_liked = post.likes.filter(user=request.user).exists()
    has_cheered = post.cheers.filter(user=request.user).exists()

    context = {
        'post': post,
        'magor': post.major,
        'comments': comments,
        'has_liked': has_liked,
        'has_cheered': has_cheered,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        post = Post.objects.create(
            author=request.user,
            major=request.user.profile.selectedMajor,  # 글쓴이 전공 자동 지정
            title=title,
            content=content,
        )
        return redirect('post_detail', post_id=post.id)

    return render(request, 'posts/post_form.html')


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