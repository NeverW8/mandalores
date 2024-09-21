from django.shortcuts import redirect
from flask_login import login_required
import requests

from json import loads
from typing import Any

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import View, TemplateView


class DiscordAuthView(View):

    def get(self, request, *args, **kwargs):
        user = authenticate(request)
        if user and user.is_authenticated:
            login(request, user)
            return redirect('/')

        redirect_uri = request.build_absolute_uri(reverse('discord_auth'))
        discord_login_url = (
            f"{settings.DISCORD_OAUTH_AUTHORIZE_ENDPIONT}"
            f"?client_id={settings.DISCORD_CLIENT_ID}"
            f"&redirect_uri={redirect_uri}"
            "&response_type=code"
            "&scope=identify"
        )
        return redirect(discord_login_url)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
