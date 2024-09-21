from django.shortcuts import redirect

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import RedirectURLMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import View, TemplateView


class LoginView(TemplateView):
    template_name = 'login.html'


class DiscordAuthView(RedirectURLMixin, View):

    next_page = '/'

    def get(self, request, *args, **kwargs):
        user = authenticate(request)
        if user and user.is_authenticated:
            login(request, user)
            return redirect(request.session['next_page'])

        request.session['next_page'] = self.get_success_url()

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
