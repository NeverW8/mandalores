from typing import Any
from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest, HttpResponseBadRequest
from django.urls import reverse
import requests
import logging

from mandalores.models import DiscordUser, create_user_and_discord_user


logger = logging.getLogger(__name__)


class DiscordOAuth2AuthorizationBackend(ModelBackend):

    def authenticate(self, request: HttpRequest, **kwargs: Any) -> AbstractBaseUser | None:
        if request.user and request.user.is_authenticated:
            return request.user

        if 'error' in request.GET or 'code' not in request.GET:
            return None

        logger.error(f'X-Forwarded-Host: {request.META.get("X-Forwarded-Host")}')
        logger.error(f'X-Forwarded-Proto: {request.META.get("X-Forwarded-Proto")}')
        code = request.GET['code']

        redirect_uri = f"https://{request.get_host()}{reverse('discord_auth')}"

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
        }

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(
            f'{settings.DISCORD_API_ENDPOINT}/oauth2/token',
            data=data,
            headers=headers,
            auth=(settings.DISCORD_CLIENT_ID, settings.DISCORD_CLIENT_SECRET)
        )
        if response.status_code != 200:
            print('Error fetching token:', response.text)
            return None

        tokens = response.json()
        access_token = tokens.get('access_token')
        if not access_token:
            return None

        user_info_response = requests.get(
            f'{settings.DISCORD_API_ENDPOINT}/users/@me',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        if user_info_response.status_code != 200:
            print('Error fetching user info:', user_info_response.text)
            return None

        user_info = user_info_response.json()
        user_data = {
            'id': user_info['id'],
            'username': user_info['username'],
            'avatar': user_info['avatar'],
        }

        try:
            discord_user = DiscordUser.objects.get(discord_id=user_data['id'])
            user = discord_user.model_user
        except DiscordUser.DoesNotExist:
            user, discord_user = create_user_and_discord_user(
                username=user_data['username'],
                discord_id=user_data['id']
            )

        return user
