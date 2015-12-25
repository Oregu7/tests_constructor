# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0002_auto_20151219_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='point',
            field=models.IntegerField(default=0),
        ),
    ]
