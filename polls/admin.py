from django.contrib import admin

from .models import Poll


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

