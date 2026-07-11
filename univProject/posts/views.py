from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Post, Comment, PostLike


def list(request):
    posts = Post.objects.select_related('author').annotate(
        like_count=Count('likes', distinct=True),
        comment_count=Count('comments', distinct=True),
    )
    return render(request, 'posts/list.html', {'posts': posts})


@login_required
def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Post.objects.create(title=title, content=content, author=request.user)
        return redirect('posts:list')
    return render(request, 'posts/create.html')


def detail(request, id):
    post = get_object_or_404(
        Post.objects.select_related('author'), id=id
    )

    view_session_key = f'viewed_post_{id}'
    if not request.session.get(view_session_key, False):
        post.views += 1
        post.save()
        request.session[view_session_key] = True

    is_liked = False
    if request.user.is_authenticated:
        is_liked = PostLike.objects.filter(post=post, user=request.user).exists()

    comments = post.comments.filter(parent=None).select_related('author').prefetch_related(
        'replies__author'
    )

    return render(request, 'posts/detail.html', {
        'post': post,
        'is_liked': is_liked,
        'comments': comments,
    })


@login_required
def update(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)  # 작성자 본인만 수정 가능
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('posts:detail', id)
    return