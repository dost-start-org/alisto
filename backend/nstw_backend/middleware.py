"""
Custom middleware to separate session-based authentication (for Django admin)
from token-based authentication (for API endpoints).
"""

from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.middleware.csrf import CsrfViewMiddleware


class ConditionalSessionMiddleware(SessionMiddleware):
    """
    Only enable session middleware for Django admin paths.
    API endpoints should remain stateless and use token authentication only.
    """
    def process_request(self, request):
        # Only enable sessions for admin paths
        if request.path.startswith('/admin/'):
            return super().process_request(request)
        # Skip session processing for API endpoints
        return None

    def process_response(self, request, response):
        # Only process session response for admin paths
        if request.path.startswith('/admin/'):
            return super().process_response(request, response)
        return response


class ConditionalCsrfMiddleware(CsrfViewMiddleware):
    """
    Only enable CSRF protection for Django admin paths.
    API endpoints use token authentication and don't need CSRF protection.
    """
    def process_request(self, request):
        # Only enable CSRF for admin paths
        if request.path.startswith('/admin/'):
            return super().process_request(request)
        return None

    def process_view(self, request, callback, callback_args, callback_kwargs):
        # Only apply CSRF checks for admin paths
        if request.path.startswith('/admin/'):
            return super().process_view(request, callback, callback_args, callback_kwargs)
        return None


class ConditionalAuthMiddleware(AuthenticationMiddleware):
    """
    Only enable Django's session-based auth middleware for admin paths.
    API endpoints will use DRF's token authentication instead.
    """
    def process_request(self, request):
        # Only enable session-based auth for admin paths
        if request.path.startswith('/admin/'):
            return super().process_request(request)
        # For API paths, set user to AnonymousUser initially
        # DRF will handle authentication via TokenAuthentication
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()
        return None
