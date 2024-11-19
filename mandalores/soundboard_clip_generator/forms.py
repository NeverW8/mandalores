from typing import Any
from django import forms

from mandalores.soundboard_clip_generator.models import SoundClip

class TimeInput(forms.TimeInput):
    input_type = "time"
    template_name = "soundboard_clip_generator/time_input.html"


class TimeField(forms.TimeField):

    def to_python(self, value: Any | None) -> Any | None:
        value = value.strip()
        # Try to strptime against each input format.
        for format in self.input_formats:
            try:
                return self.strptime(value, format)
            except (ValueError, TypeError):
                continue
        raise forms.ValidationError(self.error_messages["invalid"], code="invalid")


class SoundBoardClipGeneratorForm(forms.Form):
    url = forms.URLField()
    start_time = TimeField(input_formats=['%H:%M:%S'])
    stop_time = TimeField(input_formats=['%H:%M:%S'])

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['start_time'].widget = TimeInput()
        self.fields['stop_time'].widget = TimeInput()

    def clean(self) -> None:
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        stop_time = cleaned_data.get('stop_time')
        if start_time and stop_time and not ( start_time < stop_time):
            raise forms.ValidationError('Start time must be before stop time')

        # Check if we have this exact clip already
        url = cleaned_data.get('url')
        if SoundClip.objects.filter(
            url=url,
            start_time=start_time,
            stop_time=stop_time,
        ).exists():
            raise forms.ValidationError('That exact clip already exists')
