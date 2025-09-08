from django.shortcuts import render, get_object_or_404,redirect
from movies.models import Movie
from django.utils.text import slugify
def addphim_page(request):
    movies = Movie.objects.all()
    context={
        'movies':movies,
    }
    return render(request, "addphim_page.html",context)
def changepassword_page(request):
    return render(request, "changepassword_page.html")
def update_user_page(request):
    return render(request, "update_user_page.html")
def user(request):
    return render(request, "user.html")
def update_phim_page(request):
    return render(request, "update_phim_page.html")

from datetime import datetime

def addphim(request):
    if request.method == "POST":
        title = request.POST.get("title")
        titleE = request.POST.get("titleE")
        summary = request.POST.get("summary")
        poster_url = request.POST.get("poster_url")
        video_url = request.POST.get("video_url")
        release_date_str = request.POST.get("release_date")
        type_value = request.POST.get("type")

        release_date = None
        if release_date_str:
            try:
                release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
            except ValueError:
                release_date = None

        movie = Movie(
            title=title,
            titleE=titleE or "No Title",
            summary=summary,
            poster_url=poster_url,
            video_url=video_url,
            release_date=release_date,
            type=type_value or "No Title",
        )
        movie.save()

        return redirect(request.META.get("HTTP_REFERER", "/"))

def update_phim_page(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    context = {
        'movie': movie,
    }
    return render(request, "update_phim_page.html", context)


from datetime import datetime

def update_phim(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    if request.method == "POST":
        movie.title = request.POST.get("title")
        movie.titleE = request.POST.get("titleE")
        movie.summary = request.POST.get("summary")
        movie.poster_url = request.POST.get("poster_url")
        movie.video_url = request.POST.get("video_url")

        release_date_str = request.POST.get("release_date")
        if release_date_str:
            try:
                movie.release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
            except ValueError:
                movie.release_date = None
        else:
            movie.release_date = None

        movie.type = request.POST.get("category")

        # tạo slug mới
        year = movie.release_date.year if movie.release_date else ""
        movie.slug = slugify(f"{movie.title}-{year}")

        movie.save()
        return redirect("/admin/addphim_page")

def delete_phim(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    movie.delete()
    # Sau khi xoá thì quay lại danh sách phim hoặc trang admin
    return redirect("/admin/addphim_page")