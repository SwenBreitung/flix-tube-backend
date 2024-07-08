from django.utils.deprecation import MiddlewareMixin

class CustomCookieMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path == '/registrierung/':  
            response.set_cookie('my_cookie', 'cookie_value', httponly=False)
        return response