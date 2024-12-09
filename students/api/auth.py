from functools import wraps
from django.http import JsonResponse
from django.conf import settings

def require_api_key(view_func):
    @wraps(view_func)
    def decorated_view(request, *args, **kwargs):
        # Check for API key in both header and query parameters
        api_key = request.headers.get('X-API-Key') or request.GET.get('api_key')
        
        if not api_key:
            return JsonResponse({
                'error': 'API key is missing',
                'detail': 'Please provide an API key using X-API-Key header or api_key query parameter'
            }, status=401)
        
        if api_key != settings.API_KEY:
            return JsonResponse({
                'error': 'Invalid API key',
                'detail': 'The provided API key is not valid'
            }, status=401)
        
        return view_func(request, *args, **kwargs)
    return decorated_view