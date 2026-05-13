from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from forum.models import Topic, Post

class Like(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Mỗi user chỉ like 1 lần

    def __str__(self):
        return f'{self.user} liked {self.post}'


class Vote(models.Model):
    VOTE_CHOICES = [(1, 'Up'), (-1, 'Down')]
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    topic      = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='votes')
    value      = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'topic')

    def __str__(self):
        return f'{self.user} voted {self.value} on {self.topic}'
    