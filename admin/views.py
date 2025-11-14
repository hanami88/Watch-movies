from django.shortcuts import render, get_object_or_404,redirect
from movies.models import Movie
from users.models import Users
from django.utils.text import slugify
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
def changepassword(request):
    return render(request, "changepassword_page.html")
def user(request):
    users= Users.objects.all()
    context={
        'users':users,
    }
    return render(request, "user.html",context)

def addphim(request):
    print(f"DEBUG - User ID: {request.session.get('user_id')}")
    print(f"DEBUG - Is superuser: {request.session.get('is_superuser')}")
    print(f"DEBUG - Current URL: {request.path}")
    if request.method == "POST":
        title = request.POST.get("title")
        titleE = request.POST.get("titleE")
        summary = request.POST.get("summary")
        poster_url = request.POST.get("poster_url")
        video_url = request.POST.get("video_url")
        release_date_str = request.POST.get("release_date")
        type_value = request.POST.get("type")
        series_value = request.POST.get("series")
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
            series=series_value,
        )
        movie.save()

        return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        movies = Movie.objects.all()
        context = {
            'movies': movies,
        }
        return render(request, "addphim_page.html", context)

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
        return redirect("/admin/addphim")
    else:
        context = {
            'movie': movie,
        }
        return render(request, "update_phim_page.html", context)

def delete_phim(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    movie.delete()
    # Sau khi xoá thì quay lại danh sách phim hoặc trang admin
    return redirect("/admin/addphim")
def dangxuat(request):
    logout(request)  # Tự động xóa session và cookie
    return redirect('/login')  # Chuyển về trang chủ hoặc trang login
def delete_user(request, id):
    user = get_object_or_404(Users, id=id)
    user.delete()
    return redirect("/admin/user")
def update_user(request, id):
    user = get_object_or_404(Users, id=id)
    if request.method == "POST":
        # Lấy dữ liệu form
        name = request.POST.get("name")
        email = request.POST.get("email")
        birthday = request.POST.get("birthday")
        gender = request.POST.get("gender")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user.name = name
        user.email = email
        user.birthday = birthday
        user.gender = gender
        if new_password:
            if new_password == confirm_password:
                user.password = new_password
                messages.success(request, "Đổi mật khẩu thành công!")
            else:
                messages.error(request, "Mật khẩu xác nhận không khớp!")
        user.save()
        return redirect("/admin/user")

    return render(request, "update_user_page.html", {"user": user})