from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(user_email):
    send_mail(
        'Welcome to Mentorship!',
        'Thank you for registering at our platform.',
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )
