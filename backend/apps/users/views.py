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
        return Response(UserResponseSerializer(request.user).data)

    def patch(self, request):
        ser = UserResponseSerializer(request.user, data=request.data, partial=True)

        if ser.is_valid():
            ser.save()
            return Response(ser.data)

        return Response(ser.errors, status=400)

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
            user = ser.validated_data["user"]
            session_id = ser.validated_data["session_id"]

            return Response({
                "user": UserResponseSerializer(user).data,
                "session_id": session_id,
                "message": "2FA code sent"
            })

        return Response(ser.errors, status=400)


# Вью для підтвердження 2FA коду
class Verify2FAView(APIView):
    def post(self, request):
        ser = Verify2FASerializer(data=request.data)

        if ser.is_valid():
            return Response(ser.save())

        return Response(ser.errors, status=400)