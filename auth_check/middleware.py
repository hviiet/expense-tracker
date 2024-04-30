from django.shortcuts import render
from expense_crud.models import User

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.path in ['/login/', '/register/', '/logout/']:
            response = self.get_response(request)
            return response
        cookie_name = 'cookie'
        if cookie_name not in request.COOKIES:
            return render(request, 'login.html', {
                'server_message': 'Phiên đăng nhập đã hết hạn. Bạn cần đăng nhập để truy cập trang này.'
            })
        cookie = request.COOKIES[cookie_name]
        user = User.objects.filter(cookie=cookie).first()
        if not user:
            return render(request, 'login.html', {
                'server_message': 'Phiên đăng nhập đã hết hạn. Bạn cần đăng nhập để truy cập trang này.'
            })
        request.user = user
        response = self.get_response(request)
        return response
