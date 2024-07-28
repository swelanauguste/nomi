import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import RegistrationKey


def send_registration_email(user_email):
    key = str(uuid.uuid4())
    RegistrationKey.objects.create(key=key)

    registration_url = settings.SITE_URL + reverse(
        "unique_registration", kwargs={"key": key}
    )

    subject = "Your Registration Link"
    message = f"Please use the following link to register: {registration_url}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
