from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from forum.models import Post, Topic
from .models import Like, Vote

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'count': post.likes.count()})
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
            user_vote = 0
        else:
            vote.value = value
            vote.save()
            user_vote = value
    else:
        user_vote = value
    
    total = sum(v.value for v in topic.votes.all())
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'user_vote': user_vote, 'total': total})
    return redirect('forum:topic_detail', pk=topic_id)