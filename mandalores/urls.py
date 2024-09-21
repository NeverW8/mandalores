"""
URL configuration for mandalores project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, reverse
from django.views.generic.base import RedirectView
from django.views.decorators.csrf import requires_csrf_token

# To force the /admin page to always redirect to the login and never show the form
# if the user completes the authorization and is a staff the admin page then loads
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
admin.site.login = staff_member_required(admin.site.login, login_url=settings.LOGIN_URL)

from mandalores.views import (
    DiscordAuthView,
    HomeView,
    LoginView,
)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('discord/auth/', requires_csrf_token(DiscordAuthView.as_view()), name='discord_auth'),
    path('admin/', admin.site.urls),
]
