from django.db import models


class Poll(models.Model):

    name = models.CharField(
        'Poll name',
        help_text='Specify name of the poll',
        max_length=255,
        blank=True,
    )

    description = models.TextField(
        'Poll Description',
        help_text='Specify description for the poll',
        max_length=255,
        blank=True,
    )
    
    date_created = models.DateTimeField(
        'Date created / Poll start date',
        auto_now_add=True,
    )

    date_end = models.DateTimeField(
        ' Poll end date',
        auto_now=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Poll'
        verbose_name_plural = 'Polls'

    def __str__(self):
        return f'Poll #{self.id} - {self.name}'
