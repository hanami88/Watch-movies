from django.db import models
from movies.models import Movie

class Users(models.Model):
    name = models.CharField(max_length=255)   # tên người dùng
    password = models.CharField(max_length=255)   # mật khẩu (lưu hash, không lưu plaintext)
    birthday = models.DateField(blank=True, null=True)   # ngày sinh
    email = models.EmailField(unique=True)   # email, nên unique
    date_joined = models.DateTimeField(auto_now_add=True)  # ngày tạo tài khoản
    is_active = models.BooleanField(default=True)   # tài khoản còn hoạt động hay bị khóa
    is_superuser = models.BooleanField(default=False)  # có phải admin hay không
    gender = models.CharField(
        max_length=10,
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        blank=True,
        null=True
    )
    sdt = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return self.name

class UsersFavoriteMovies(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="favorite_movies")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="liked_by_users")
    added_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'movie'], name='unique_user_movie')
        ]
    def __str__(self):
        return f"{getattr(self.user, 'name', 'Unknown')} ❤️ {getattr(self.movie, 'title', 'Unknown')}"

class UsersCommentMovies(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="movie_comments")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "users_comment_movies"
        ordering = ["-created_at"]
    def __str__(self):
        return f"{self.user.name} - {self.movie.title}: {self.content[:30]}"


