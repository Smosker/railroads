# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trains_schedule', '0006_auto_20160223_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='destination_city',
            field=models.ForeignKey(related_name='s_destination_city_name', to='trains_schedule.City'),
        ),
    ]
