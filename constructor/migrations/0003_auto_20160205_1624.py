# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0002_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='category',
            field=models.ForeignKey(to='constructor.Category', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='questions_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
