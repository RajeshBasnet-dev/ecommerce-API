from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import BlacklistedToken
import jwt
from django.conf import settings

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that checks for blacklisted tokens.
    """
    
    def authenticate(self, request):
        try:
            # Get the token from the request
            header = self.get_header(request)
            if header is None:
                return None

            raw_token = self.get_raw_token(header)
            if raw_token is None:
                return None

            # Validate the token
            validated_token = self.get_validated_token(raw_token)
            
            # Check if token is blacklisted
            jti = validated_token.get('jti')
            if jti and BlacklistedToken.objects.filter(jti=jti).exists():
                raise InvalidToken('Token is blacklisted')
            
            # Return the user
            return self.get_user(validated_token), validated_token
        except InvalidToken:
            return None
        except Exception:
            return None