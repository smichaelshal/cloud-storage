from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
        Reset password from email, sends an email with a password verification token.
    """
    
    email_plaintext_message = f"""
    The code is {reset_password_token.key} to user {reset_password_token.user.username}
    """

    send_mail(
        # title:
        "Password Reset for {title} {usernames}".format(title="Some website title", usernames=reset_password_token.user.username),
        # message:
        f'{email_plaintext_message}',
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
