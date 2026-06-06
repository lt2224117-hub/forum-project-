from django.urls import path, re_path
from . import views

app_name = 'interaction'

urlpatterns = [
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    re_path(r'^vote/(?P<topic_id>\d+)/(?P<value>-?\d+)/$', views.vote_topic, name='vote_topic'),
]