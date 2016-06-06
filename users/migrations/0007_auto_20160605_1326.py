# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-05 10:26
from __future__ import unicode_literals

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20160605_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='secret_key',
            field=models.CharField(default=users.models.Group.generate_secret_code, editable=False, max_length=25, unique=True),
        ),
    ]