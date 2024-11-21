from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client


@shared_task
def send_ticket_email(user_email, order_info):
    send_mail(
        'Информация о заказе',
        order_info,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False
    )


@shared_task
def send_sms(to_phone, info):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=info,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to_phone
    )