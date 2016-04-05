# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0003_auto_20160207_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='probationer',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
