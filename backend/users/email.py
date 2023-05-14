import random
from django.core.mail import send_mail
from django.conf import settings

from .models import CustomUser

def send_otp_via_email(recipient_email):
    subject = "Invoicy - Your Email Verification OTP"

    otp = random.randint(1000, 9999)
    message = f"Here is your OTP - {otp}"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient_email]
    )

    user = CustomUser.objects.get(email = recipient_email)
    user.otp = otp
    user.save()