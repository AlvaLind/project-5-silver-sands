from django.utils.cache import patch_cache_control

class NoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Prevent caching of authenticated views
        if request.user.is_authenticated:
            patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True)
        return response
