# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0002_auto_20160201_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='probationer',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
