from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .utils import Util


class AnonUser(AbstractUser):
    """Custom Anon user model based on IP address"""

    @property
    def hashed_ip(self):
        return Util.hash_string_ip(self.ip_address)

    ip_address = models.GenericIPAddressField(
        protocol='IPv4',
        default='127.0.0.1',
        unique=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Anon User'
        verbose_name_plural = 'Anon Users'

    def __str__(self):
        return f'{self.hashed_ip}'


class Poll(models.Model):

    @property
    def is_open(self):
        return self.date_end > timezone.now()

    owner = models.ForeignKey(AnonUser, on_delete=models.CASCADE)

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
        'Poll end date',
        default=Util.close_date(days=7),
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Poll'
        verbose_name_plural = 'Polls'

    def __str__(self):
        return f'#{self.id} - {self.name}'


class Choice(models.Model):
    poll = models.ForeignKey(
        Poll,
        related_name='choice',
        on_delete=models.CASCADE
    )

    text = models.CharField(
        'Choice Text',
        max_length=255
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'

    def __str__(self):
        return f'{self.text}'


class Vote(models.Model):
    user = models.ForeignKey(
        AnonUser,
        related_name='vote',
        on_delete=models.CASCADE
    )

    poll = models.ForeignKey(
        Poll,
        related_name='vote',
        on_delete=models.CASCADE
    )

    choice = models.ForeignKey(
        Choice,
        related_name='vote',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'

    def __str__(self):
        return f'{self.poll.name[:15]} - {self.choice.text[:15]}'
