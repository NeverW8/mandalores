from typing import Any, Mapping
from django import forms
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList

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
    end_time = TimeField(input_formats=['%H:%M:%S'])

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['start_time'].widget = TimeInput()
        self.fields['end_time'].widget = TimeInput()

    def clean(self) -> None:
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time and end_time and not ( start_time < end_time):
            raise forms.ValidationError('Start time must be before stop time')
