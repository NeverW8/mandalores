from django.urls import path

from mandalores.soundboard_clip_generator.views import GenerateClip

app_name = 'soundboard'

urlpatterns = [
    path('generate/', GenerateClip.as_view(), name='generate_clip'),
]