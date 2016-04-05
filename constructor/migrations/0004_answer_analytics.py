# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0003_auto_20160205_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='analytics',
            field=models.IntegerField(default=0),
        ),
    ]
