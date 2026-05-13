from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from forum.models import Topic, Post
from django.contrib.auth.models import User

@staff_member_required
def dashboard(request):
    total_topics = Topic.objects.count()
    total_posts = Post.objects.count()
    total_users = User.objects.count()
    recent_topics = Topic.objects.order_by('-created_at')[:10]
    return render(request, 'moderation/dashboard.html', {
        'total_topics': total_topics,
        'total_posts': total_posts,
        'total_users': total_users,
        'recent_topics': recent_topics,
    })

@staff_member_required
def pin_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    topic.is_pinned = not topic.is_pinned
    topic.save()
    messages.success(request, f'{"Đã ghim" if topic.is_pinned else "Bỏ ghim"} chủ đề!')
    return redirect('forum:topic_detail', pk=pk)

@staff_member_required
def lock_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    topic.is_locked = not topic.is_locked
    topic.save()
    messages.success(request, f'{"Đã khóa" if topic.is_locked else "Mở khóa"} chủ đề!')
    return redirect('forum:topic_detail', pk=pk)

@staff_member_required
def hide_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    topic_pk = post.topic.pk
    post.delete()
    messages.success(request, 'Đã ẩn bài viết!')
    return redirect('forum:topic_detail', pk=topic_pk)