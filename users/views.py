from django.shortcuts import render, get_object_or_404,redirect
from movies.models import Movie


def information(request):
    user = getattr(request, "user_custom", None)
    user_favorites = []
    if user:
        user_favorites = Movie.objects.filter(liked_by_users__user=user.id)
    context = {
        "user": user,
        "user_favorites": user_favorites,
    }
    return render(request, "information.html", context)
def save(request):
    user = getattr(request, "user_custom", None)
    if request.method == "POST" and user:
        # Cập nhật các trường từ form
        user.name = request.POST.get("name", user.name)
        user.birthday = request.POST.get("birthday") or None
        user.gender = request.POST.get("gender") or None
        user.sdt = request.POST.get("sdt", "")  # nếu bạn có field sdt trong model
        user.email = request.POST.get("email", user.email)
        # Lưu thay đổi
        user.save()
        return redirect("/user/information")  # quay lại trang thông tin
    # Nếu không phải POST thì quay về trang trước
    return redirect(request.META.get("HTTP_REFERER", "/"))

