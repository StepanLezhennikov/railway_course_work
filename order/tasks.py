from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_ticket_email(user_email, order_info):
    send_mail(
        'Информация о заказе',
        order_info,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False
    )
