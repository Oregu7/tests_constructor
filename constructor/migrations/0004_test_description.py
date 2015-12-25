# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0003_auto_20151219_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
