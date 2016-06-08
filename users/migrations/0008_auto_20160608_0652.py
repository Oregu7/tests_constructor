# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-08 03:52
from __future__ import unicode_literals

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20160605_1326'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='specialization',
            options={'verbose_name': 'Специализацию', 'verbose_name_plural': 'Специализации'},
        ),
        migrations.AlterField(
            model_name='group',
            name='secret_key',
            field=models.CharField(default=users.models.Group.generate_secret_code, editable=False, max_length=25, unique=True, verbose_name='Секретный код'),
        ),
        migrations.AlterField(
            model_name='specialization',
            name='code',
            field=models.CharField(max_length=200, primary_key=True, serialize=False, unique=True, verbose_name='Код'),
        ),
        migrations.AlterField(
            model_name='specialization',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
    ]