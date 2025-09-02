from django.db import models
from django.utils.text import slugify
class Movie(models.Model):
    title = models.CharField(max_length=255)
    titleE = models.CharField(max_length=255,default="No Title")   # tên phim
    summary = models.TextField(blank=True, null=True)    # tóm tắt
    poster_url = models.URLField(blank=True, null=True)  # link poster
    video_url = models.CharField(max_length=255)   # link video/stream
    release_date = models.DateField(blank=True, null=True)  # ngày phát hành
    created_at = models.DateTimeField(auto_now_add=True)    # tạo lúc nào
    updated_at = models.DateTimeField(auto_now=True)        # cập nhật lúc nào
    views = models.IntegerField(default=0)
    nomination = models.BooleanField(default=False)
    type=models.CharField(max_length=255,default="No Title")
    slug = models.SlugField(unique=True, blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.title)}-{self.year}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

