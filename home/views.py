from django.shortcuts import render, redirect
from movies.models import Movie as movie
from django.contrib import messages
from users.models import Users
from django.contrib.auth.hashers import check_password

def get_home(request):
    movies = movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request, 'home.html', context)

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
        if password == user.password:
            # Lưu user vào session
            request.session["user_id"] = user.id
            request.session["is_superuser"] = user.is_superuser

            if user.is_superuser:
                messages.success(request, "Đăng nhập thành công (Admin)")
                return render(request, "loginpage.html")  # chuyển sang trang admin
            else:
                messages.success(request, "Đăng nhập thành công (User)")
                return render(request, "loginpage.html")   # chuyển sang trang user
        else:
            messages.error(request, "Mật khẩu cặc")
            return render(request, "loginpage.html")
    else:
        return render(request, "loginpage.html")