from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name        = models.CharField(max_length=100, verbose_name='Tên chuyên mục')
    description = models.TextField(blank=True, verbose_name='Mô tả')
    slug        = models.SlugField(unique=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Chuyên mục'
        verbose_name_plural = 'Chuyên mục'

    def __str__(self):
        return self.name


class Topic(models.Model):
    title       = models.CharField(max_length=200, verbose_name='Tiêu đề')
    content     = models.TextField(verbose_name='Nội dung')
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')
    category    = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='topics')
    is_pinned   = models.BooleanField(default=False, verbose_name='Ghim')
    is_locked   = models.BooleanField(default=False, verbose_name='Khóa')
    views       = models.PositiveIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    TAG_CHOICES = [
        ('thac_mac', 'Thắc mắc'),
        ('thao_luan', 'Thảo luận'),
        ('danh_gia', 'Đánh giá'),
        ('chia_se', 'Chia sẻ'),
        ('huong_dan', 'Hướng dẫn'),
        ]
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, blank=True, null=True, verbose_name='Tag')

    class Meta:
        verbose_name = 'Chủ đề'
        verbose_name_plural = 'Chủ đề'
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title


class Post(models.Model):
    topic      = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    author     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content    = models.TextField(verbose_name='Nội dung')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Bài viết'
        verbose_name_plural = 'Bài viết'
        ordering = ['created_at']

    def __str__(self):
        return f'Post by {self.author} in {self.topic}'