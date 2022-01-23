from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AnonUser, Answer, Choice, Poll, Vote


@admin.register(AnonUser)
class CustomUserAdmin(UserAdmin):

    list_per_page = 50
    list_display = (
        'id',
        'ip_address',
        'username',
    )
    empty_value_display = '-empty-'

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('ip_address',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('ip_address',)}),
    )


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


@admin.register(Answer)
class Answer(admin.ModelAdmin):
    list_per_page = 50
    list_display = (
        'user',
        'poll',
        'text',
    )
    empty_value_display = '-empty-'
