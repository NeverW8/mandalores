from django.urls import path

from mandalores.media_material.views import (
    MediaPlaceholderView,
)

app_name = 'media_material'

urlpatterns = [
    path('', MediaPlaceholderView.as_view(), name='index'),
]
