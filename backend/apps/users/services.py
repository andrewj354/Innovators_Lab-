# services.py
import redis
from random import randint
from django.conf import settings
from django.core.mail import send_mail


# Підключення до Redis
r = redis.StrictRedis(
    host=getattr(settings, "REDIS_HOST", "localhost"),
    port=getattr(settings, "REDIS_PORT", 6379),
    db=0,
    decode_responses=True
)

def code_generate():
    """Генерує 6-значний код 2FA"""
    return f"{randint(100000, 999999)}"

def set_2fa_code(user_id):
    """Зберігає код 2FA у Redis на 5 хвилин"""
    code = code_generate()
    key = f"2fa:{user_id}"
    r.setex(key, 300, code) 
    return code

def verify_2fa_code(user_id, code):
    """Перевіряє код 2FA та видаляє його після успішної перевірки"""
    key = f"2fa:{user_id}"
    stored_code = r.get(key)
    if stored_code == code:
        r.delete(key)
        return True
    return False

def send_code(email, code):
    # subject = "Your 2FA Code"
    # message = f"Your verification code is: {code}"

    # send_mail(
    #     subject,
    #     message,
    #     None,          # from email (візьме DEFAULT_FROM_EMAIL)
    #     [email],
    #     fail_silently=False,
    # )

    print(f"{email} - {code}")


