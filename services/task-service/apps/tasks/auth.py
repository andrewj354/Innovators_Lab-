from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken


class MockUser:
    """Mock user object for microservices that don't have local user database."""
    def __init__(self, user_id, email, username=''):
        self.id = user_id
        self.pk = user_id
        self.email = email
        self.username = username or f'user_{user_id}'
        self.is_authenticated = True
        self.is_active = True
        self.is_staff = False
        self.is_superuser = False


class JWTAuthenticationWithoutDatabase(JWTAuthentication):
    """
    JWT Authentication that doesn't require user to exist in local database.
    Used in microservices architecture where each service has its own user table.
    The JWT token is issued by user-service and contains user_id that proves identity.
    """
    
    def authenticate(self, request):
        """
        Validate JWT token from Authorization header without requiring
        the user to exist in this service's database.
        """
        # Get the JWT token
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return None
            
        token = auth_header[7:]  # Remove 'Bearer ' prefix
        
        try:
            # Validate the token
            validated_token = self.get_validated_token(token)
            
            # Extract user info from token (user_id from JWT payload)
            user_id = validated_token.get('user_id')
            if not user_id:
                raise InvalidToken('Token does not contain user_id')
            
            # Create a mock user object that represents the authenticated user
            # We don't need to fetch from database - JWT proves identity
            user = MockUser(
                user_id=user_id,
                email=validated_token.get('email', ''),
                username=validated_token.get('username', f'user_{user_id}')
            )
            
            return (user, validated_token)
            
        except AuthenticationFailed:
            raise
        except InvalidToken:
            raise
        except Exception as e:
            raise AuthenticationFailed(f'Token validation failed: {str(e)}')


class TokenRequiredPermission:
    """
    Permission class that only requires a valid JWT token.
    Used when we don't need to validate user existence in local database.
    """
    
    message = 'Valid JWT token required'
    
    def has_permission(self, request, view):
        # Check if we have an authenticated user (with is_authenticated=True)
        return bool(request.user and request.user.is_authenticated)
