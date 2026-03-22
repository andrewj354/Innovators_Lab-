from random import randint
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings


def code_generate():
    """Генерує 6-значний код 2FA"""
    return f"{randint(100000, 999999)}"


def set_2fa_code(user_id):
    if cache.get(f"2fa_block:{user_id}"):
        raise Exception("Too many requests")

    code = code_generate()
    cache.set(f"2fa:{user_id}", code, timeout=300)
    cache.set(f"2fa_block:{user_id}", True, timeout=60)  # 1 хв cooldown
    return code


def verify_2fa_code(user_id, code):
    """Перевіряє код і видаляє після використання"""
    key = f"2fa:{user_id}"
    stored_code = cache.get(key)

    if stored_code and stored_code == code:
        cache.delete(key)
        return True

    return False


def send_code(email, code):
    """Відправка 2FA коду на email"""

    subject = "Your 2FA Code"
    message = f"Your verification code is: {code}"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )