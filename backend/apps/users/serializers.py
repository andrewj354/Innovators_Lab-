from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
from .services import create_2fa_session, verify_2fa_session, send_code
from rest_framework_simplejwt.tokens import RefreshToken


# --- Реєстрація ---
class UserRegistrationsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Паролі не збігаються"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = CustomUser.objects.create_user(**validated_data)
        return user


# --- Логін ---
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')

        if not email or not password:
            raise serializers.ValidationError("Вкажи email і password")

        user = authenticate(request=request, username=email, password=password)

        if not user:
            raise serializers.ValidationError("Користувача не знайдено")
        if not user.is_active:
            raise serializers.ValidationError("Користувач не активний")

        try:
            session_id, code = create_2fa_session(user.id)
        except Exception as e:
            raise serializers.ValidationError(str(e))

        try:
            send_code(user.email, code)
        except Exception:
            pass

        return {
            "user": user,
            "session_id": session_id
        }


# --- Підтвердження 2FA ---
class Verify2FASerializer(serializers.Serializer):
    session_id = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        user_id = verify_2fa_session(data['session_id'], data['code'])

        if not user_id:
            raise serializers.ValidationError("Невірний або прострочений код")

        data['user_id'] = user_id
        return data

    def save(self):
        user = CustomUser.objects.get(id=self.validated_data['user_id'])

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


# --- Відповідь користувачу ---
class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'role',
        ]
        read_only_fields = ['email', 'role']