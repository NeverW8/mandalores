from typing import Any

from django.db import transaction
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
from django.urls import reverse
from django.views.generic import FormView, TemplateView, View
from django.shortcuts import get_object_or_404


from mandalores.soundboard_clip_generator.forms import SoundBoardClipGeneratorForm
from mandalores.soundboard_clip_generator.models import SoundClip
from mandalores.soundboard_clip_generator.utils import downloadClip


class GenerateClip(LoginRequiredMixin, FormView):
    template_name = 'soundboard_clip_generator/soundboard_clip_generator.html'

    success_url = 'soundboard:clip_with_id'

    form_class = SoundBoardClipGeneratorForm

    def form_valid(self, form: SoundBoardClipGeneratorForm) -> HttpResponse:
        with transaction.atomic():
            sound_clip = SoundClip.objects.create(
                url=form.cleaned_data.get('url'),
                start_time=form.cleaned_data.get('start_time'),
                stop_time=form.cleaned_data.get('stop_time'),
            )
            # For local dev we perform the download and processing inline
            if settings.DEBUG:
                downloadClip(sound_clip)
            return HttpResponseRedirect(
                reverse(self.success_url, kwargs={'clip_id': sound_clip.id})
            )


class ClipView(LoginRequiredMixin, TemplateView):
    template_name = 'soundboard_clip_generator/clip_details.html'

    def get_context_data(self, clip_id) -> dict[str, Any]:
        context =  super().get_context_data()
        context['clip'] = get_object_or_404(SoundClip, id=clip_id)
        return context


class ClipDetails(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, clip_id=None, **kwargs) -> HttpResponse:
        clip = get_object_or_404(SoundClip, id=clip_id)
        return JsonResponse(
            {
                'status': clip.status,
            }
        )

class ClipDownloader(LoginRequiredMixin, View):

    def get(self, request, clip_id):
        clip = get_object_or_404(SoundClip, id=clip_id)
        return FileResponse(clip.file.file, as_attachment=True)
