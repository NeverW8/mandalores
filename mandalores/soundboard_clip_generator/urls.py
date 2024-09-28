from django.urls import path

from mandalores.soundboard_clip_generator.views import (
    ClipDetails,
    ClipDownloader,
    GenerateClip,
    ClipView,
)

app_name = 'soundboard'

urlpatterns = [
    path('<int:clip_id>', ClipView.as_view(), name='clip_with_id'),
    path('api/clip/<int:clip_id>', ClipDetails.as_view(), name='clip_details'),
    path('generate/', GenerateClip.as_view(), name='generate_clip'),
    path('download/<int:clip_id>', ClipDownloader.as_view(), name='download'),
]