from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from movies.models import Movie
from .models import Users  # Import model Users
def information(request):
    """
    View hiển thị thông tin cá nhân và phim yêu thích
    """
    # Lấy user_id từ session
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "Vui lòng đăng nhập để xem thông tin")
        return redirect('/login/')

    try:
        user = Users.objects.get(id=user_id)
        # Lấy danh sách phim yêu thích
        user_favorites = Movie.objects.filter(liked_by_users__user=user.id)
    except Users.DoesNotExist:
        messages.error(request, "Người dùng không tồn tại")
        request.session.flush()  # Xóa session không hợp lệ
        return redirect('/login/')

    context = {
        "user_favorites": user_favorites,
        # Không cần truyền user vì context processor đã có
    }
    return render(request, "information.html", context)


def save(request):
    """
    View lưu thông tin cá nhân đã chỉnh sửa
    """
    # Lấy user_id từ session
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "Vui lòng đăng nhập để thực hiện thao tác này")
        return redirect('/login/')

    if request.method == "POST":
        try:
            user = Users.objects.get(id=user_id)

            # Cập nhật các trường từ form
            user.name = request.POST.get("name", user.name)

            # Xử lý birthday (có thể là chuỗi rỗng)
            birthday = request.POST.get("birthday")
            if birthday:
                user.birthday = birthday

            # Xử lý gender
            gender = request.POST.get("gender")
            if gender:
                user.gender = gender

            # Xử lý số điện thoại (nếu có field này)
            sdt = request.POST.get("sdt", "")
            if hasattr(user, 'sdt'):  # Kiểm tra xem có field sdt không
                user.sdt = sdt

            # Cập nhật email
            email = request.POST.get("email", user.email)
            if email and email != user.email:
                # Kiểm tra email đã tồn tại chưa
                if Users.objects.filter(email=email).exclude(id=user.id).exists():
                    messages.error(request, "Email đã được sử dụng bởi tài khoản khác")
                    return redirect("/user/information")
                user.email = email

            # Lưu thay đổi
            user.save()
            messages.success(request, "Cập nhật thông tin thành công!")

        except Users.DoesNotExist:
            messages.error(request, "Người dùng không tồn tại")
            request.session.flush()
            return redirect('/login/')
        except Exception as e:
            messages.error(request, f"Có lỗi xảy ra: {str(e)}")

        return redirect("/user/information")

    # Nếu không phải POST request
    messages.warning(request, "Phương thức không hợp lệ")
    return redirect("/user/information")


def change_password(request):
    """
    View đổi mật khẩu (bonus)
    """
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "Vui lòng đăng nhập để thực hiện thao tác này")
        return redirect('/login/')

    if request.method == "POST":
        try:
            user = Users.objects.get(id=user_id)

            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            # Kiểm tra mật khẩu cũ
            if old_password != user.password:
                messages.error(request, "Mật khẩu cũ không đúng")
                return render(request, "change_password.html")

            # Kiểm tra mật khẩu mới
            if not new_password:
                messages.error(request, "Vui lòng nhập mật khẩu mới")
                return render(request, "change_password.html")

            # Kiểm tra xác nhận mật khẩu
            if new_password != confirm_password:
                messages.error(request, "Xác nhận mật khẩu không khớp")
                return render(request, "change_password.html")

            # Cập nhật mật khẩu
            user.password = new_password  # Nên hash password trong thực tế
            user.save()

            messages.success(request, "Đổi mật khẩu thành công!")
            return redirect("/user/information")

        except Users.DoesNotExist:
            messages.error(request, "Người dùng không tồn tại")
            request.session.flush()
            return redirect('/login/')
        except Exception as e:
            messages.error(request, f"Có lỗi xảy ra: {str(e)}")

    return render(request, "change_password.html")