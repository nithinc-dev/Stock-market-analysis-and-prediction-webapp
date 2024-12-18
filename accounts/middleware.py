# accounts/middleware.py
from django.utils import timezone
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin

class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            last_login = request.session.get('last_login', None)
            if last_login:
                current_time = timezone.now().timestamp()
                elapsed_time = current_time - last_login
                if elapsed_time > 5 * 60 * 60:  # 5 hours in seconds
                    logout(request)
                    return