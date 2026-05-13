from django.urls import path
from . import views

app_name = 'interaction'

urlpatterns = [
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('vote/<int:topic_id>/<str:value>/', views.vote_topic, name='vote_topic'),
]