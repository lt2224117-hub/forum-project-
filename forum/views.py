from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Category, Topic, Post

def home(request):
    categories = Category.objects.all()
    sort = request.GET.get('sort', 'new')
    if sort == 'popular':
        recent_topics = Topic.objects.select_related('author', 'category').annotate(
            post_count=Count('posts')
        ).order_by('-post_count', '-created_at')[:10]
    else:
        recent_topics = Topic.objects.select_related('author', 'category').order_by('-created_at')[:10]
    return render(request, 'forum/home.html', {
        'categories': categories,
        'recent_topics': recent_topics,
        'sort': sort,
    })
def explore(request):
    tag = request.GET.get('tag', '')
    sort = request.GET.get('sort', 'hot')
    
    categories = Category.objects.annotate(topic_count=Count('topics')).order_by('-topic_count')
    
    topics = Topic.objects.select_related('author', 'category').annotate(
        post_count=Count('posts')
    )
    if tag:
        topics = topics.filter(tag=tag)
    
    if sort == 'new':
        topics = topics.order_by('-created_at')[:20]
    else:
        topics = topics.order_by('-views', '-post_count')[:20]

    # Đề xuất: chuyên mục có nhiều chủ đề nhất
    suggested_categories = categories[:6]

    TAG_CHOICES = [
        ('thac_mac', 'Thắc mắc'),
        ('thao_luan', 'Thảo luận'),
        ('danh_gia', 'Đánh giá'),
        ('chia_se', 'Chia sẻ'),
        ('huong_dan', 'Hướng dẫn'),
    ]

    return render(request, 'forum/explore.html', {
        'categories': categories,
        'suggested_categories': suggested_categories,
        'topics': topics,
        'sort': sort,
        'tag': tag,
        'tag_choices': TAG_CHOICES,
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    sort = request.GET.get('sort', 'new')
    if sort == 'popular':
        topics = category.topics.select_related('author').annotate(
            post_count=Count('posts')
        ).order_by('-is_pinned', '-post_count', '-created_at')
    else:
        topics = category.topics.select_related('author').order_by('-is_pinned', '-created_at')
    return render(request, 'forum/category_detail.html', {
        'category': category,
        'topics': topics,
        'sort': sort,
    })

def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    topic.views += 1
    topic.save()
    posts = topic.posts.select_related('author').all()

    if request.method == 'POST' and request.user.is_authenticated and not topic.is_locked:
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if content:
            Post.objects.create(topic=topic, author=request.user, content=content, image=image)
            messages.success(request, 'Đã gửi bình luận!')
            return redirect('forum:topic_detail', pk=pk)

    return render(request, 'forum/topic_detail.html', {
        'topic': topic,
        'posts': posts,
    })

@login_required
def topic_create(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tag = request.POST.get('tag', '')
        image = request.FILES.get('image')
        if title and content:
            topic = Topic.objects.create(
                title=title, content=content,
                author=request.user, category=category,
                tag=tag, image=image
            )
            messages.success(request, 'Tạo chủ đề thành công!')
            return redirect('forum:topic_detail', pk=topic.pk)
    return render(request, 'forum/topic_form.html', {'category': category})

@login_required
def topic_edit(request, pk):
    topic = get_object_or_404(Topic, pk=pk, author=request.user)
    if request.method == 'POST':
        topic.title = request.POST.get('title')
        topic.content = request.POST.get('content')
        image = request.FILES.get('image')
        if image:
            topic.image = image
        topic.save()
        messages.success(request, 'Cập nhật thành công!')
        return redirect('forum:topic_detail', pk=topic.pk)
    return render(request, 'forum/topic_form.html', {'topic': topic, 'category': topic.category})

@login_required
def topic_delete(request, pk):
    topic = get_object_or_404(Topic, pk=pk, author=request.user)
    if request.method == 'POST':
        topic.delete()
        messages.success(request, 'Đã xóa chủ đề!')
        return redirect('forum:home')
    return render(request, 'forum/topic_confirm_delete.html', {'topic': topic})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.content = request.POST.get('content')
        image = request.FILES.get('image')
        if image:
            post.image = image
        post.save()
        messages.success(request, 'Cập nhật bài viết thành công!')
        return redirect('forum:topic_detail', pk=post.topic.pk)
    return render(request, 'forum/post_form.html', {'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    topic_pk = post.topic.pk
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Đã xóa bài viết!')
        return redirect('forum:topic_detail', pk=topic_pk)
    return render(request, 'forum/post_confirm_delete.html', {'post': post})