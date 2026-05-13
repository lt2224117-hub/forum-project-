from django.contrib import admin
from .models import Category, Topic, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_pinned', 'is_locked', 'views', 'created_at']
    list_filter = ['category', 'is_pinned', 'is_locked']
    search_fields = ['title', 'content']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'topic', 'created_at']
    search_fields = ['content']


