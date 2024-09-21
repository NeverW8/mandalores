import requests

from json import loads
from typing import Any

from django.conf import settings
from django.contrib.auth import login
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View, TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie

from django_discord_oauth2.views import discord_callback

from mandalores.models import DiscordUser, create_user_and_discord_user


# The django-discord-oauth2 package does not do a reverse on the
# DISCORD_POST_URL so it has to be an absolute URL with protocol.
# To alleviate that we override the default callback with a wrapper
@ensure_csrf_cookie
def discord_overriden_callback(request: HttpRequest):
    response: JsonResponse = discord_callback(request)
    post_response = requests.post(
        request.build_absolute_uri(reverse(settings.DISCORD_AUTH_ENDPOINT)),
        # Rebuild the content into a JSON dict
        json=loads(response.content)
    )
    if post_response.status_code != 200:
        return HttpResponseForbidden()
    response = HttpResponseRedirect(redirect_to=reverse('home'))
    for key, value in post_response.cookies.items():
        response.set_cookie(key, value)
    return response


class DiscordAuthView(View):

    success_url = '/'

    def post(self, request: HttpRequest, *args, **kwargs):
        json_data = loads(request.body)
        try:
            discord_user = DiscordUser.objects.get(discord_id=json_data['id'])
            user = discord_user.model_user
        except DiscordUser.DoesNotExist:
            user, discord_user = create_user_and_discord_user(
                username=json_data['username'],
                email=json_data['email'],
                discord_id=json_data['id']
            )
        login(self.request, user)
        return HttpResponse()


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)
