# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20151216_2046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('helps', models.BooleanField()),
                ('time_completion', models.IntegerField()),
                ('public_access', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('two_mark', models.IntegerField()),
                ('three_mark', models.IntegerField()),
                ('four_mark', models.IntegerField()),
                ('creator', models.ForeignKey(to='users.Users')),
            ],
        ),
    ]
