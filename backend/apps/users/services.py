
import random

# Генерація коду
def code_generate():
    code =random.randint(100000,999999)
    return code


def send_code(email,code):

    # send_mail(
    #     'Your activation code',
    #     f'Code: {code}',
    #     '123456@gmail.com',#Ваша пошта,
    #     [email]
    # )