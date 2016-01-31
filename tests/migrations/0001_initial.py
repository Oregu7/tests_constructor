# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0007_auto_20160125_1041'),
    ]

    operations = [
        migrations.CreateModel(
            name='Probationer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('mark', models.IntegerField()),
                ('precent', models.IntegerField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('test', models.ForeignKey(to='constructor.Test')),
            ],
        ),
    ]
