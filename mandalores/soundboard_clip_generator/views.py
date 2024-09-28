from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from mandalores.soundboard_clip_generator.forms import SoundBoardClipGeneratorForm

class GenerateClip(LoginRequiredMixin, FormView):
    template_name = 'soundboard_clip_generator/soundboard_clip_generator.html'

    form_class = SoundBoardClipGeneratorForm

    def form_valid(self, form: Any) -> HttpResponse:
        print("FORM VALID!")
        return super().form_valid(form)
