from django.utils.deprecation import MiddlewareMixin
from users.models import Users

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.session.get("user_id")
        if user_id:
            try:
                user = Users.objects.get(id=user_id)
                request.user_custom = user
            except Users.DoesNotExist:
                request.user_custom = None
        else:
            request.user_custom = None
