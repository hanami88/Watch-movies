from django.shortcuts import render, redirect, get_object_or_404
from users.models import UsersFavoriteMovies
from users.models import Users
from .models import Movie
from django.http import JsonResponse
from django.contrib import messages
from users.models import UsersCommentMovies
from django.db.models import Q, Case, When, IntegerField
def xemphim(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    comments = UsersCommentMovies.objects.filter(movie=movie).select_related("user")
    movies = Movie.objects.filter(
        Q(series=movie.series) | Q(type=movie.type)
    ).exclude(id=movie.id).order_by(
        Case(
            When(series=movie.series, then=0),
            default=1,
            output_field=IntegerField()
        )
    )
    movie.views += 1
    movie.save(update_fields=["views"])
    is_liked = False
    if getattr(request, "user", None):
        is_liked = UsersFavoriteMovies.objects.filter(
            user=request.user, movie=movie
        ).exists()  # Chỉ kiểm tra movie hiện tại

    context = {
        'movies': movies,
        'movie': movie,
        'is_liked': is_liked,  # Boolean thay vì list
        'comments': comments,
    }
    return render(request, 'xemphim.html', context)

def thich(request, slug):
    if request.method == 'POST':
        try:
            user = request.user  # Đã có từ middleware
            movie = get_object_or_404(Movie, slug=slug)

            # Kiểm tra đã thích chưa
            favorite = UsersFavoriteMovies.objects.filter(user=user, movie=movie).first()

            if favorite:
                # Đã thích → bỏ thích
                favorite.delete()
                liked = False
            else:
                # Chưa thích → thích
                UsersFavoriteMovies.objects.create(user=user, movie=movie)
                liked = True
            return JsonResponse({
                'success': True,
                'liked': liked,
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
            })
    return JsonResponse({
        'success': False,
    })

def comment(request, slug):
    if request.method == "POST":
        movie = get_object_or_404(Movie, slug=slug)
        # Lấy nội dung bình luận
        content = request.POST.get("comment", "").strip()
        if not content:
            return redirect(request.META.get("HTTP_REFERER", f"/xemphim/{movie.slug}"))
        # Tạo comment mới
        UsersCommentMovies.objects.create(
            user=request.user,
            movie=movie,
            content=content
        )
        return redirect(request.META.get("HTTP_REFERER", f"/xemphim/{movie.slug}"))
    return JsonResponse({"error": "Phương thức không hợp lệ"}, status=405)

