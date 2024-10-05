from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView, View


class EmojiPlaceholderView(LoginRequiredMixin, TemplateView):
    template_name = 'emoji_resizer/emoji_resizer.html'
