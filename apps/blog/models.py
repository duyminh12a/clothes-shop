from django.db import models
from core.models import TimeStampedModel
from django.utils.text import slugify

class BlogCategory(TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name="Tên chuyên mục")
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Chuyên mục blog"
        verbose_name_plural = "Chuyên mục blog"


class BlogPost(TimeStampedModel):
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name="posts", verbose_name="Chuyên mục")
    title = models.CharField(max_length=250, verbose_name="Tiêu đề bài viết")
    slug = models.SlugField(max_length=270, unique=True, blank=True)
    excerpt = models.TextField(blank=True, verbose_name="Tóm tắt ngắn")
    content = models.TextField(verbose_name="Nội dung bài viết (HTML / Markdown)")
    cover_image = models.ImageField(upload_to="blog/", blank=True, null=True, verbose_name="Ảnh bìa")
    cover_url = models.CharField(max_length=500, blank=True, verbose_name="Hoặc URL ảnh bìa")
    is_published = models.BooleanField(default=True, verbose_name="Xuất bản")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Lượt đọc")

    def get_cover(self):
        if self.cover_image:
            return self.cover_image.url
        return self.cover_url or ""

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Bài viết"
        verbose_name_plural = "Bài viết blog"
        ordering = ['-created_at']
