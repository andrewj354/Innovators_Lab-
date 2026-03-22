# serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
from .services import set_2fa_code, verify_2fa_code, send_code

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
            raise serializers.ValidationError('Потрібно вказати "email" та "password"')

        user = authenticate(request=request, username=email, password=password)
        if not user:
            raise serializers.ValidationError("Користувача не знайдено")
        if not user.is_active:
            raise serializers.ValidationError("Користувач не активний")

        # Генерація 2FA коду та збереження у Redis
        attrs['user'] = user
        code = set_2fa_code(user.id)
        send_code(email=user.email, code=code)
        return attrs

# --- Підтвердження 2FA ---
class Verify2FASerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField()

    def validate(self, data):
        if not verify_2fa_code(data['user_id'], data['code']):
            raise serializers.ValidationError("Невірний або прострочений код")
        return data

    def save(self):
        user = CustomUser.objects.get(id=self.validated_data['user_id'])
        login(self.context['request'], user)
        return {"detail": "Успішний логін"}

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