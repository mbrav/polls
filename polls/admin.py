from django.contrib import admin

from .models import Choice, Poll, Vote


@admin.register(Poll)
class Poll(admin.ModelAdmin):
    list_per_page = 50
    list_display = (
        'id',
        'name',
        'description',
        'date_created',
        'date_end',
    )
    empty_value_display = '-empty-'


@admin.register(Choice)
class Choice(admin.ModelAdmin):
    list_per_page = 50
    list_display = (
        'poll',
        'text',
    )
    empty_value_display = '-empty-'


@admin.register(Vote)
class Vote(admin.ModelAdmin):
    list_per_page = 50
    list_display = (
        'user',
        'poll',
        'choice',
    )
    empty_value_display = '-empty-'
