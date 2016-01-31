# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='probationer',
            name='precent',
            field=models.FloatField(),
        ),
    ]
