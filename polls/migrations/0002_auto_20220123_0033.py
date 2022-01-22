# Generated by Django 3.2.11 on 2022-01-22 21:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='type',
            field=models.CharField(choices=[('1', 'Choice'), ('2', 'Multichoice'), ('3', 'Answer')], default='1', max_length=1),
        ),
        migrations.AlterField(
            model_name='poll',
            name='date_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 29, 21, 33, 32, 190328, tzinfo=utc), verbose_name='Poll end date'),
        ),
    ]
