from django.core.exceptions import ValidationError
from django.db import models


class SoundClip(models.Model):
    PENDING_STATUS = 'pending'
    COMPLETED_STATUS = 'completed'
    FAILED_STATUS = 'failed'
    url = models.URLField(null=False, blank=False)
    start_time = models.TimeField(null=False, blank=False)
    stop_time = models.TimeField(null=False, blank=False)
    status = models.CharField(
        choices=[
            (PENDING_STATUS, 'Pending'),
            (COMPLETED_STATUS, 'Completed'),
            (FAILED_STATUS, 'Failed'),
        ],
        default='pending',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='clips', null=True, blank=True)


    class Meta:
        unique_together = [
            'url',
            'start_time',
            'stop_time',
        ]


    def clean(self) -> None:
        if not self.start_time < self.stop_time:
            raise ValidationError('Start time must be before stop time')

    @property
    def completed(self):
        return self.status == self.COMPLETED_STATUS

    @property
    def failed(self):
        return self.status == self.FAILED_STATUS

    @property
    def pending(self):
        return self.status == self.PENDING_STATUS

    def __str__(self):
        return f'{self.url} between {self.start_time} <-> {self.stop_time}'
