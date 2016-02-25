# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trains_schedule', '0004_auto_20160222_0148'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='destination_city',
            field=models.ForeignKey(related_name='schedule_destination_city_name', default=2, to='trains_schedule.City'),
            preserve_default=False,
        ),
    ]
