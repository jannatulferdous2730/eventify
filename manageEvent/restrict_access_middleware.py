from django.shortcuts import redirect


# Restrict access to specific paths
class RestrictAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        restricted_paths = ['/dashboard/', '/update-password/', '/cancel_booking/', '/success/', '/cancel_booking/']
        if request.path in restricted_paths and not request.user.is_authenticated:
            return redirect('/')
        return self.get_response(request)
