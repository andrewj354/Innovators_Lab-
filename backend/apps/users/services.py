import uuid
from random import randint
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings


def code_generate():
    return f"{randint(100000, 999999)}"


def create_2fa_session(user_id):
    """Створює 2FA сесію і повертає session_id"""
    session_id = str(uuid.uuid4())

    if cache.get(f"2fa_block:{user_id}"):
        raise Exception("Too many requests")

    code = code_generate()

    cache.set(f"2fa_code:{session_id}", code, timeout=300)
    cache.set(f"2fa_user:{session_id}", user_id, timeout=300)
    cache.set(f"2fa_block:{user_id}", True, timeout=60)

    return session_id, code


def verify_2fa_session(session_id, code):
    stored_code = cache.get(f"2fa_code:{session_id}")
    user_id = cache.get(f"2fa_user:{session_id}")

    if stored_code and stored_code == code:
        cache.delete(f"2fa_code:{session_id}")
        cache.delete(f"2fa_user:{session_id}")
        return user_id

    return None


def send_code(email, code):
    subject = "Your 2FA Code"
    message = f"Your verification code is: {code}"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )