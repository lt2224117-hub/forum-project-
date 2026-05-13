from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from forum.models import Post, Topic
from .models import Like, Vote

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('forum:topic_detail', pk=post.topic.pk)

@login_required
def vote_topic(request, topic_id, value):
    topic = get_object_or_404(Topic, pk=topic_id)
    value = int(value)
    if value not in [1, -1]:
        return redirect('forum:topic_detail', pk=topic_id)
    vote, created = Vote.objects.get_or_create(
        user=request.user, topic=topic,
        defaults={'value': value}
    )
    if not created:
        if vote.value == value:
            vote.delete()
        else:
            vote.value = value
            vote.save()
    return redirect('forum:topic_detail', pk=topic_id)