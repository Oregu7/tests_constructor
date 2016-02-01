# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('text', models.CharField(blank=True, max_length=200)),
                ('correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('text', models.TextField()),
                ('help', models.TextField(blank=True)),
                ('time', models.IntegerField(default=5)),
                ('point', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('helps', models.BooleanField(default=False)),
                ('time_completion', models.BooleanField(default=False)),
                ('public_access', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('two_mark', models.IntegerField()),
                ('three_mark', models.IntegerField()),
                ('four_mark', models.IntegerField()),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='query',
            name='test',
            field=models.ForeignKey(to='constructor.Test'),
        ),
        migrations.AddField(
            model_name='answer',
            name='query',
            field=models.ForeignKey(to='constructor.Query'),
        ),
    ]
