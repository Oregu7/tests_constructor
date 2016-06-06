# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-05 10:14
from __future__ import unicode_literals

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_group_secret_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='secret_key',
            field=models.CharField(default=users.models.Group.generate_secret_code, max_length=25),
        ),
    ]
