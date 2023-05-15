from django.core.mail import send_mail
from django.conf import settings

def send_reminder_via_email(recipient_email, message):
    subject = "Invoicy - Reminder to pay your bill"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient_email]
    )