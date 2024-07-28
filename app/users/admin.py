import uuid

from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail
from django.urls import reverse

from .models import Profile, RegistrationInvitation, User


def send_registration_email(email, key):
    registration_url = settings.SITE_URL + reverse(
        "unique_registration", kwargs={"key": key}
    )

    subject = "Your Registration Link"
    message = f"Please use the following link to register: {registration_url}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])


@admin.action(description="Send registration invitation email")
def send_registration_invitations(modeladmin, request, queryset):
    for invitation in queryset:
        if not invitation.used:
            send_registration_email(invitation.email, invitation.key)
            modeladmin.message_user(
                request, f"Registration email sent to {invitation.email}"
            )
        else:
            modeladmin.message_user(
                request,
                f"Invitation for {invitation.email} has already been used.",
                level="error",
            )


class RegistrationInvitationAdmin(admin.ModelAdmin):
    list_display = ("email", "sent_at", "used")
    actions = [send_registration_invitations]


admin.site.register(RegistrationInvitation, RegistrationInvitationAdmin)


admin.site.register(User)
admin.site.register(Profile)
