from django.shortcuts import render, redirect, get_object_or_404
from users.models import UsersFavoriteMovies
from users.models import Users
from .models import Movie
from django.http import JsonResponse
from django.contrib import messages
from users.models import UsersCommentMovies
def xemphim(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    comments = UsersCommentMovies.objects.filter(movie=movie).select_related("user")
    movies = Movie.objects.all()
    movie.views += 1
    movie.save(update_fields=["views"])
    user_favorites = []
    if getattr(request, "user_custom", None):
        user_favorites = UsersFavoriteMovies.objects.filter(
            user=request.user_custom
        ).values_list("movie", flat=True)
    context = {
        'movies': movies,
        'movie': movie,
        'user': getattr(request, "user_custom", None),
        'user_favorites': user_favorites,
        'comments':comments,
    }
    return render(request, 'xemphim.html', context)


def thich(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        movie_id = request.POST.get("movie_id")
        if not movie_id:
            return JsonResponse({"error": "Thiếu movie_id"}, status=400)
        try:
            movie = get_object_or_404(Movie, id=movie_id)
        except Exception as e:
            return JsonResponse({"error": f"Không tìm thấy phim: {str(e)}"}, status=404)

        user = getattr(request, "user_custom", None)

        if not user:
            return JsonResponse({"error": "Chưa đăng nhập"}, status=403)

        favorite, created = UsersFavoriteMovies.objects.get_or_create(
            user=user,
            movie=movie
        )
        if not created:
            favorite.delete()
            liked = False
        else:
            liked = True

        return JsonResponse({"liked": liked})

    return JsonResponse({"error": "Phải gửi POST AJAX"}, status=400)

def comment(request, slug):
    if request.method == "POST":
        movie = get_object_or_404(Movie, slug=slug)

        user_id = request.session.get("user_id")
        if not user_id:
            # Nếu chưa login thì chuyển tới trang đăng nhập
            return redirect("/loginpage")
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return redirect("/loginpage")

        # Lấy nội dung bình luận
        content = request.POST.get("comment", "").strip()
        if not content:
            return redirect(request.META.get("HTTP_REFERER", f"/xemphim/{movie.slug}"))

        # Tạo comment mới
        UsersCommentMovies.objects.create(
            user=user,
            movie=movie,
            content=content
        )
        return redirect(request.META.get("HTTP_REFERER", f"/xemphim/{movie.slug}"))
    return JsonResponse({"error": "Phương thức không hợp lệ"}, status=405)

