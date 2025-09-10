from django.shortcuts import render, redirect
from movies.models import Movie as movie
from django.contrib import messages
from users.models import Users
from rest_framework_simplejwt.tokens import RefreshToken
from users.views import information
from django.contrib.auth.hashers import check_password

def get_home(request):
    movies = movie.objects.all()
    movies_list = movie.objects.all().order_by('-views')[:10]
    context = {
        "movies": movies,
        "movies_list": movies_list,
    }
    return render(request, "home.html", context)


def login_page(request):
    return render(request, 'loginpage.html')

def register_page(request):
    return render(request, 'registerpage.html')

def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        repassword = request.POST.get("repassword")
        # Kiểm tra độ dài mật khẩu
        if len(password) < 8:
            messages.error(request, "Mật khẩu phải có ít nhất 8 ký tự!")
            return render(request, "registerpage.html")
        # Kiểm tra mật khẩu trùng khớp
        if password != repassword:
            messages.error(request, "Mật khẩu nhập lại không khớp!")
            return render(request, "registerpage.html")
        # Kiểm tra email đã tồn tại chưa
        if Users.objects.filter(email=email).exists():
            messages.error(request, "Email này đã được đăng ký!")
            return render(request, "registerpage.html")
        # Tạo user mới
        user = Users.objects.create(
            email=email,
            password=password  # ❌ thực tế nên hash (bcrypt), đây demo thôi
        )
        return redirect("/loginpage")  # về trang login chẳng hạn

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            messages.error(request, "Email không tồn tại")
            return render(request, "loginpage.html")
        if password==user.password:
            request.session["user_id"] = user.id
            request.session["is_superuser"] = user.is_superuser
            if user.is_superuser:
                return redirect("/admin/addphim")
            else:
                return redirect("/user/information")
        else:
            messages.error(request, "Mật khẩu không đúng")
            return render(request, "loginpage.html")

    return render(request, "loginpage.html")

def logout(request):
    request.session.flush()
    return redirect('/')