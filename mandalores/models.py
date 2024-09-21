from django.conf import settings
from django.db import models

class DiscordUser(models.Model):
    model_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    discord_id = models.CharField(
        unique=True,
    )
    discord_username = models.CharField(
        unique=True,
    )
    discord_email = models.EmailField()
