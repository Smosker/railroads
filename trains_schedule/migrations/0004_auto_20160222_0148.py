# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trains_schedule', '0003_auto_20160222_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='departure_city',
            field=models.ForeignKey(related_name='schedule_departure_city_name', to='trains_schedule.City'),
        ),
    ]
