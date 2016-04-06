# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specialization',
            name='id',
        ),
        migrations.AlterField(
            model_name='specialization',
            name='code',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]
