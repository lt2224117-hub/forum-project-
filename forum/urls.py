from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.home, name='home'),
    path('explore/', views.explore, name='explore'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('topic/create/<slug:category_slug>/', views.topic_create, name='topic_create'),
    path('topic/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('topic/<int:pk>/edit/', views.topic_edit, name='topic_edit'),
    path('topic/<int:pk>/delete/', views.topic_delete, name='topic_delete'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
]