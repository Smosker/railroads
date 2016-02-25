# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trains_schedule', '0005_schedule_destination_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='departure_city',
            field=models.ForeignKey(related_name='s_departure_city_name', to='trains_schedule.City'),
        ),
    ]
