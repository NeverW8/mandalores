from django.urls import path

from mandalores.emoji_resizer.views import (
    EmojiPlaceholderView,
)

app_name = 'emoji_resizer'

urlpatterns = [
    path('', EmojiPlaceholderView.as_view(), name='index'),
]
