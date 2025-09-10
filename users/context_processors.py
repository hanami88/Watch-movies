from .models import Users  # Import model Users của bạn
def user_context(request):
    """
    Context processor để thêm thông tin user vào mọi template
    """
    context = {
        'user': None,
        'is_user_logged_in': False,
        'is_current_user_superuser': False,
    }

    if hasattr(request, 'session'):
        user_id = request.session.get('user_id')

        if user_id:
            try:
                # Lấy thông tin user từ database
                user = Users.objects.get(id=user_id)
                context.update({
                    'user': user,  # Toàn bộ object user
                    'is_user_logged_in': True,
                    'is_current_user_superuser': user.is_superuser,
                })
            except Users.DoesNotExist:
                # Nếu user không tồn tại, xóa session
                request.session.flush()

    return context