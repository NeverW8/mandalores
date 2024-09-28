from django.urls import path

from mandalores.soundboard_clip_generator.views import (
    GenerateClip,
    ClipView,
)

app_name = 'soundboard'

urlpatterns = [
    path('<int:clip_id>', ClipView.as_view(), name='clip_with_id'),
    path('generate/', GenerateClip.as_view(), name='generate_clip'),
]