from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.conf import settings

class APIKeyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Only check API key for API endpoints
        if request.path.startswith('/api/'):
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
            
            # Store the validated API key in request for later use if needed
            request.api_key = api_key