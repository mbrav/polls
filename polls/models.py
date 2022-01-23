from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .utils import Util


class AnonUser(AbstractUser):
    """Custom Anon user model based on IP address"""

    ip_address = models.GenericIPAddressField(
        protocol='IPv4',
        default='127.0.0.1',
        unique=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Anon User'
        verbose_name_plural = 'Anon Users'

    def __str__(self):
        return f'{self.username}'


@receiver(pre_save, sender=AnonUser)
def set_username(sender, instance, *args, **kwargs):
    """Set AnonUser's username to hash of IP address"""

    instance.username = Util.hash_string_ip(instance.ip_address)


class Poll(models.Model):

    POLL_TYPES = (
        ('1', 'Choice'),
        ('2', 'Multichoice'),
        ('3', 'Answer'),
    )

    @property
    def is_open(self):
        return Util.date_is_future(self.date_end)

    owner = models.ForeignKey(AnonUser, on_delete=models.CASCADE)

    type = models.CharField(
        max_length=1,
        default='1',
        choices=POLL_TYPES
    )

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

    @property
    def owner(self):
        return self.user

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


class Answer(models.Model):

    @property
    def owner(self):
        return self.user

    user = models.ForeignKey(
        AnonUser,
        related_name='answer',
        on_delete=models.CASCADE
    )

    poll = models.ForeignKey(
        Poll,
        related_name='answer',
        on_delete=models.CASCADE
    )

    text = models.CharField(
        'Answer Text',
        max_length=255
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return f'{self.poll.name[:15]} - {self.text[:15]}'
