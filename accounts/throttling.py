from rest_framework.throttling import SimpleRateThrottle
from django.core.cache import cache
import time

class AuthRateThrottle(SimpleRateThrottle):
    """
    Rate throttle for authentication endpoints.
    """
    scope = 'auth'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return None  # Only throttle unauthenticated requests

        ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

class LoginRateThrottle(AuthRateThrottle):
    """
    Specific throttle for login attempts.
    """
    scope = 'login'

class RegisterRateThrottle(AuthRateThrottle):
    """
    Specific throttle for registration attempts.
    """
    scope = 'register'

class PasswordResetRateThrottle(AuthRateThrottle):
    """
    Specific throttle for password reset attempts.
    """
    scope = 'password_reset'