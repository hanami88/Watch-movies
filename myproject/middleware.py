from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from users.models import Users
class AuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware xử lý xác thực và phân quyền người dùng
    """
    # Danh sách các URL không cần đăng nhập
    EXEMPT_URLS = [
        '/login',
        '/register',
        '/logout',
        '/static',
        '/media',
        '/',  # trang chủ
        '/loginpage',  # Sửa lỗi syntax
        '/registerpage',
        '/xemphim/<slug:slug>',
    ]

    # Danh sách các URL chỉ admin mới được truy cập
    ADMIN_REQUIRED_URLS = [
        '/admin/',  # Thay đổi này - bắt tất cả URL bắt đầu bằng /admin/
    ]

    # Danh sách các URL chỉ user thường được truy cập (admin BỊ CẤM)
    USER_ONLY_URLS = [  # Đổi tên từ USER_REQUIRED_URLS
        '/user/',  # Bắt tất cả URL bắt đầu bằng /user/
        '/xemphim/<slug:slug>/thich',
        '/xemphim/<slug:slug>/comment',
    ]

    def is_exempt_url(self, url):
        """
        Kiểm tra xem URL có được miễn kiểm tra không
        """
        for exempt_url in self.EXEMPT_URLS:
            if url == exempt_url:
                return True
        if url.startswith('/xemphim/') and len(url.split('/')) <=2:
            return True  # /xemphim/slug/ hoặc /xemphim/slug/comment/
        return False

    def is_admin_required_url(self, url):
        """
        Kiểm tra xem URL có yêu cầu quyền admin không
        """
        for admin_url in self.ADMIN_REQUIRED_URLS:
            if url.startswith(admin_url):
                return True
        return False

    def is_user_only_url(self, url):  # Đổi tên method
        """
        Kiểm tra xem URL có yêu cầu chỉ user thường được truy cập không
        """
        for user_url in self.USER_ONLY_URLS:
            if url.startswith(user_url):
                return True
        return False

    def process_request(self, request):
        current_url = request.path
        # Bỏ qua kiểm tra cho các URL trong danh sách exempt
        # Kiểm tra xem user đã đăng nhập chưa
        user_id = request.session.get('user_id')
        is_superuser = request.session.get('is_superuser', False)
        if self.is_exempt_url(current_url):
            if not is_superuser:
                return None
            else:
                return redirect('/admin/addphim')

        try:
            user = Users.objects.get(id=user_id)
            request.user = user  # ĐÂY RỒI!
        except Users.DoesNotExist:
            request.session.flush()
            return redirect('/login')

        # Kiểm tra quyền truy cập admin
        if self.is_admin_required_url(current_url):
            if not is_superuser:
                return redirect('/')

        # Kiểm tra URL chỉ dành cho user thường (admin bị cấm)
        if self.is_user_only_url(current_url):
            if is_superuser==1:
                return redirect('/admin/addphim')
            elif not is_superuser==0:
                return redirect('/')
        return None

