from django.urls import path
from . import views

app_name = 'moderation'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('topic/<int:pk>/pin/', views.pin_topic, name='pin_topic'),
    path('topic/<int:pk>/lock/', views.lock_topic, name='lock_topic'),
    path('post/<int:pk>/hide/', views.hide_post, name='hide_post'),
]