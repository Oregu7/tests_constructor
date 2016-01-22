# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0004_test_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='time',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='query',
            name='point',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='test',
            name='helps',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='test',
            name='time_completion',
            field=models.BooleanField(default=False),
        ),
    ]
