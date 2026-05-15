from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
import secrets
import pyotp
from apps.users.models import User, PasswordResetToken
from apps.users.serializers import UserWithProfileSerializer
from django.core.mail import send_mail
from django.conf import settings


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {'error': 'Email and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # pass the email key to authenticate so backends using
    # USERNAME_FIELD='email' pick it up correctly
    user = authenticate(request, email=email, password=password)
    if user and user.is_active:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'two_fa_enabled': user.two_fa_enabled,
            }
        })

    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    try:
        # accept several possible field names for the refresh token
        refresh_token = (
            request.data.get('refresh') or
            request.data.get('refresh_token') or
            request.data.get('token')
        )
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken(refresh_token)
        return Response({
            'access': str(refresh.access_token),
        })
    except Exception as e:
        return Response(
            {'error': 'Invalid refresh token'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """Get current user profile"""
    serializer = UserWithProfileSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password_view(request):
    """Request password reset"""
    email = request.data.get('email')
    
    if not email:
        return Response(
            {'error': 'Email is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(email=email)
        # Generate reset token
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(hours=24)
        
        PasswordResetToken.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
        
        reset_link = f"{request.META.get('HTTP_ORIGIN', 'http://localhost:3000')}/reset-password?token={token}"
        
        # Send email (optional)
        # send_mail(
        #     'Password Reset Request',
        #     f'Click here to reset your password: {reset_link}',
        #     settings.DEFAULT_FROM_EMAIL,
        #     [email],
        #     fail_silently=True,
        # )
        
        return Response({
            'message': 'Password reset link sent to email',
            'token': token  # Include token for development/testing
        })
    except User.DoesNotExist:
        return Response({
            'message': 'If email exists, reset link has been sent'
        })


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_view(request):
    """Reset password with token"""
    token = request.data.get('token')
    new_password = request.data.get('new_password')
    
    if not token or not new_password:
        return Response(
            {'error': 'Token and new password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
        
        if not reset_token.is_valid():
            return Response(
                {'error': 'Reset token is invalid or expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = reset_token.user
        user.set_password(new_password)
        user.save()
        
        reset_token.is_used = True
        reset_token.save()
        
        return Response({'message': 'Password reset successfully'})
    except PasswordResetToken.DoesNotExist:
        return Response(
            {'error': 'Invalid reset token'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enable_2fa_view(request):
    """Generate 2FA secret"""
    user = request.user
    
    # Generate secret key
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(
        name=user.email,
        issuer_name='Innovators Lab'
    )
    
    return Response({
        'secret': secret,
        'qr_code_uri': provisioning_uri,
        'message': 'Scan this QR code with your authenticator app'
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_2fa_view(request):
    """Verify and enable 2FA"""
    user = request.user
    code = request.data.get('code')
    secret = request.data.get('secret')
    
    if not code or not secret:
        return Response(
            {'error': 'Code and secret are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        totp = pyotp.TOTP(secret)
        if totp.verify(code):
            user.two_fa_secret = secret
            user.two_fa_enabled = True
            user.save()
            return Response({
                'message': '2FA enabled successfully',
                'two_fa_enabled': True
            })
        else:
            return Response(
                {'error': 'Invalid verification code'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_2fa_login_view(request):
    """Verify 2FA code during login"""
    code = request.data.get('code')
    
    if not code:
        return Response(
            {'error': 'Code is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = request.user
        if not user.two_fa_enabled or not user.two_fa_secret:
            return Response(
                {'error': '2FA not enabled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        totp = pyotp.TOTP(user.two_fa_secret)
        if totp.verify(code):
            return Response({
                'message': '2FA verification successful',
                'verified': True
            })
        else:
            return Response(
                {'error': 'Invalid code'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def disable_2fa_view(request):
    """Disable 2FA"""
    user = request.user
    user.two_fa_enabled = False
    user.two_fa_secret = None
    user.save()
    
    return Response({
        'message': '2FA disabled',
        'two_fa_enabled': False
    })
