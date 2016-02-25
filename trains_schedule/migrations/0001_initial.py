# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city_name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('departure_date', models.DateTimeField(verbose_name=b'date of departure')),
                ('destination_date', models.DateTimeField(verbose_name=b'date of arriving')),
                ('departure_city', models.ForeignKey(related_name='schedule_departure_city_name', to='trains_schedule.City')),
                ('destination_city', models.ForeignKey(related_name='schedule_destination_city_name', to='trains_schedule.City')),
            ],
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('train_model', models.CharField(max_length=20)),
                ('train_type', models.CharField(max_length=10)),
                ('train_type_description', models.CharField(max_length=100)),
                ('train_capacity', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='schedule',
            name='train',
            field=models.ForeignKey(to='trains_schedule.Train'),
        ),
    ]
