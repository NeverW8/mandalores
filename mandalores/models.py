from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from requests import post

if TYPE_CHECKING:
    from django.contrib.auth.models import User


def create_user_and_discord_user(username: str, email: str, discord_id: str) -> tuple['User', 'DiscordUser']:
    if username not in settings.DISCORD_DEFAULT_ALLOWED_USERS:
        return None, None

    user = get_user_model().objects.create(
        username=discord_id,
    )
    discord_user = DiscordUser.objects.create(
        model_user=user,
        discord_id=discord_id,
        discord_email=email,
        discord_username=username
    )

    return user, discord_user


class DiscordUser(models.Model):
    model_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='discord_user',
    )
    discord_id = models.CharField(
        unique=True,
    )
    discord_username = models.CharField(
        unique=True,
    )
    discord_email = models.EmailField(
        blank=True,
        null=True,
    )


@receiver(user_logged_in)
def on_login(sender, user, request, **kwargs):
    # No webhook configured
    if not settings.DISCORD_WEBHOOK_URL:
        return
    # Not a discord user
    if not user.discord_user or not user.discord_user.discord_username:
        return
    response = post(
        settings.DISCORD_WEBHOOK_URL, json={
            'content': f'{user.discord_user.discord_username} logged in..'
        }
    )
    response.raise_for_status()
