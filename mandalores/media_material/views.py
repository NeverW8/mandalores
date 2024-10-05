from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class MediaPlaceholderView(LoginRequiredMixin, TemplateView):
    template_name = 'media_material/media.html'
