from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import code_generate, send_code
from .models import CustomUser
from .serializers import (
    UserLoginSerializer,
    UserRegistrationsSerializer,
    Verify2FASerializer,
    UserResponseSerializer
)
from rest_framework.permissions import IsAuthenticated




class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserResponseSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserResponseSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

# Вью для реєстрації користувача
class RegisterView(APIView):
    def post(self, request):
        ser = UserRegistrationsSerializer(data=request.data)
        if ser.is_valid():
            ser.save()  # створюємо користувача
            return Response({'message': 'User Register'}, status=201)
        return Response(ser.errors, status=400)


# Вью для логіну користувача
class LoginView(APIView):
    def post(self, request):
        ser = UserLoginSerializer(data=request.data, context={"request": request})
        if ser.is_valid():
            user = ser.validated_data['user']
            response_ser = UserResponseSerializer(user)

            # Повертаємо дані користувача та повідомлення про відправку 2FA коду
            return Response({
                "user": response_ser.data,
                "message": "2FA code sent"
            })
        return Response(ser.errors, status=400)


# Вью для підтвердження 2FA коду
class Verify2FAView(APIView):
    def post(self, request):
        ser = Verify2FASerializer(data=request.data, context={"request": request})
        if ser.is_valid():
            result = ser.save()  # логін користувача після підтвердження 2FA
            return Response(result)
        return Response(ser.errors, status=400)