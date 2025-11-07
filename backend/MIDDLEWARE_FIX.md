# Middleware Configuration Fix

## Problem

The application was throwing an error on deployment:

```
django.core.exceptions.ImproperlyConfigured: The session-based temporary message storage requires session middleware to be installed, and come before the message middleware in the MIDDLEWARE list.
```

This error occurred because:

1. The Django `MessageMiddleware` requires session support to store temporary messages
2. The custom `ConditionalSessionMiddleware` was skipping session initialization for non-admin paths
3. When API endpoints (like `/health/`) were accessed, the `MessageMiddleware` tried to use sessions that weren't properly initialized

## Solution

Created a `ConditionalMessageMiddleware` class that only enables the Django message framework for admin paths, matching the behavior of the other conditional middleware.

### Changes Made

#### 1. Updated `nstw_backend/middleware.py`

Added new middleware class:

```python
class ConditionalMessageMiddleware(MessageMiddleware):
    """
    Only enable message middleware for Django admin paths.
    API endpoints don't need Django's message framework.
    """
    def process_request(self, request):
        # Only enable messages for admin paths
        if request.path.startswith('/admin/'):
            return super().process_request(request)
        return None

    def process_response(self, request, response):
        # Only process message response for admin paths
        if request.path.startswith('/admin/'):
            return super().process_response(request, response)
        return response
```

#### 2. Updated `nstw_backend/settings.py`

Changed the middleware configuration:

**Before:**

```python
MIDDLEWARE = [
    ...
    'django.contrib.messages.middleware.MessageMiddleware',
    ...
]
```

**After:**

```python
MIDDLEWARE = [
    ...
    'nstw_backend.middleware.ConditionalMessageMiddleware',
    ...
]
```

## Why This Works

The application has a unique architecture where:

- **Admin paths** (`/admin/*`) use traditional Django session-based authentication
- **API paths** (`/api/*`, `/health/*`, etc.) use stateless token-based authentication

By making the `MessageMiddleware` conditional:

1. Admin pages still have full message support for Django admin notifications
2. API endpoints don't trigger the message middleware at all
3. No sessions are created or required for API endpoints
4. The error is prevented because messages are never initialized for non-admin paths

## Middleware Order

The correct order for conditional middleware is:

1. `ConditionalSessionMiddleware` - Handles sessions (admin only)
2. `ConditionalCsrfMiddleware` - Handles CSRF protection (admin only)
3. `ConditionalAuthMiddleware` - Handles authentication (admin only)
4. `ConditionalMessageMiddleware` - Handles messages (admin only)

All of these only activate for `/admin/*` paths, keeping API endpoints completely stateless.

## Testing

After deploying this fix, verify:

1. **Health endpoint works:**

   ```bash
   curl https://your-domain.com/health/
   # Should return: {"status": "healthy", "host": "..."}
   ```

2. **Admin still works:**

   - Visit `https://your-domain.com/admin/`
   - Messages should display correctly after admin actions

3. **API endpoints work:**
   - All API endpoints should function normally without session cookies
   - Token authentication should work as expected

## Additional Notes

- This fix maintains the stateless nature of the API while keeping full Django admin functionality
- No database migrations needed
- No environment variable changes required
- The fix is backward compatible with existing deployments
