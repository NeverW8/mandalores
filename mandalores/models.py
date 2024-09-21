from typing import TYPE_CHECKING
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import models
from django.contrib.auth import get_user_model


if TYPE_CHECKING:
    from django.contrib.auth.models import User


def create_user_and_discord_user(username: str, email: str, discord_id: str) -> tuple['User', 'DiscordUser']:
    if username not in settings.DISCORD_DEFAULT_ALLOWED_USERS:
        raise PermissionDenied(f'{username} not in allowed users')

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
    discord_email = models.EmailField()
