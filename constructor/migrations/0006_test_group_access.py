# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-15 18:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20160514_1249'),
        ('constructor', '0005_auto_20160515_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='group_access',
            field=models.ManyToManyField(blank=True, to='users.Group', verbose_name='Групповой доступ'),
        ),
    ]
