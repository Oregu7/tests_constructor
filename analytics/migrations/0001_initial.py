# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0004_answer_analytics'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analytic',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('answer', models.ForeignKey(to='constructor.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('code', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tested',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('course', models.IntegerField(blank=True, null=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('role', models.ForeignKey(to='analytics.Role')),
                ('specialization', models.ForeignKey(to='analytics.Specialization', blank=True, null=True)),
                ('test', models.ForeignKey(to='constructor.Test')),
            ],
        ),
        migrations.AddField(
            model_name='analytic',
            name='tested',
            field=models.ForeignKey(to='analytics.Tested'),
        ),
    ]
