# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-22 09:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0008_auto_20160519_1706'),
        ('tests', '0005_auto_20160512_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='probationer',
            name='option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='constructor.Option', verbose_name='Вариант'),
            preserve_default=False,
        ),
    ]
