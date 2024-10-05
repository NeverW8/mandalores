from threading import Thread
from typing import Any

from django.db import transaction
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
from django.urls import reverse
from django.views.generic import FormView, TemplateView, View
from django.views.generic.list import ListView
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
            # For local dev we perform the download and processing inline in a thread
            if settings.DEBUG:
                thread = Thread(target=downloadClip, args=(sound_clip,))
                thread.start()
            return HttpResponseRedirect(
                reverse(self.success_url, kwargs={'clip_id': sound_clip.id})
            )


class ClipView(LoginRequiredMixin, TemplateView):
    template_name = 'soundboard_clip_generator/clip_details.html'

    def get_context_data(self, clip_id) -> dict[str, Any]:
        context =  super().get_context_data()
        context['clip'] = get_object_or_404(SoundClip, id=clip_id)
        return context


class ClipDetailsAPI(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, clip_id=None, **kwargs) -> HttpResponse:
        clip = get_object_or_404(SoundClip, id=clip_id)
        return JsonResponse(
            {
                'status': clip.status,
                'statusDisplay': clip.get_status_display(),
                'completed': clip.completed,
                'failed': clip.failed,
                'pending': clip.pending,
            }
        )

class ClipDownloader(LoginRequiredMixin, View):

    def get(self, request, clip_id):
        clip = get_object_or_404(SoundClip, id=clip_id)
        return FileResponse(clip.file.file, as_attachment=True)


class ClipListView(LoginRequiredMixin, ListView):
    model = SoundClip
    template_name = 'soundboard_clip_generator/clips_list.html'
