from rest_framework import serializers
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
from .services import code_generate, send_code


# Серіалізатор для реєстрації користувача
class UserRegistrationsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')

    # Перевірка, чи збігаються паролі
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Паролі не збігаються"})
        return attrs

    # Створення користувача
    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = CustomUser.objects.create_user(**validated_data)
        return user


# Серіалізатор для логіну користувача
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    # Перевірка логіну
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            if not user:
                raise serializers.ValidationError("Користувача не знайдено")
            if not user.is_active:
                raise serializers.ValidationError("Користувач не активний")

            # Генерація 2FA коду та збереження у сесії
            attrs['user'] = user
            code = code_generate()
            request = self.context['request']
            request.session['2fa_user_id'] = user.id
            request.session['2fa_code'] = str(code)
            print(code)  # для тесту
            # send_code(email=email, code=code)  # можна відправляти на email
            return attrs
        else:
            raise serializers.ValidationError('Потрібно вказати "email" та "password"')


# Серіалізатор для підтвердження 2FA коду
class Verify2FASerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate(self, data):
        request = self.context['request']
        session_code = request.session.get('2fa_code')
        user_id = request.session.get('2fa_user_id')

        if session_code is None or user_id is None:
            raise serializers.ValidationError("Немає активної 2FA сесії")

        if data['code'] != session_code:
            raise serializers.ValidationError("Невірний код")

        return data

    # Логін користувача після підтвердження коду
    def save(self):
        request = self.context['request']
        user = CustomUser.objects.get(id=request.session['2fa_user_id'])

        # Очищення сесії
        request.session.pop('2fa_code')
        request.session.pop('2fa_user_id')

        login(request, user)

        return {"detail": "Успішний логін"}


# Серіалізатор для відповіді користувачу
class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email']