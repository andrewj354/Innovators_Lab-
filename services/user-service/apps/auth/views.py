from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from apps.users.models import User



import random
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(username=email, password=password)
    
    if user and user.is_active:
        otp_code = str(random.randint(1000, 9999))
        
        cache.set(f'otp_{email}', otp_code, timeout=300)
        
        print(f"DEBUG OTP for {email}: {otp_code}") 
        
        return Response({
            'message': 'Код підтвердження надіслано на email',
            'email': email  
        }, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp_view(request):
    email = request.data.get('email')
    otp_received = request.data.get('otp')

    if not email or not otp_received:
        return Response({'error': 'Email and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)

    otp_in_cache = cache.get(f'otp_{email}')

    if otp_in_cache and otp_in_cache == str(otp_received):
        cache.delete(f'otp_{email}')
        user = User.objects.get(email=email)
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email
            }
        })

    return Response({'error': 'Невірний або прострочений код'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error':'Refresh token is required'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken(refresh_token)
        return Response({
            'access':str(refresh.access_token),
        })
    except Exception as e:
        return Response(
            {'error':'Invalid refresh token'},
            status =status.HTTP_401_UNAUTHORIZED
        )