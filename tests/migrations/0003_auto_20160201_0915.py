# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tests', '0002_auto_20160131_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='probationer',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=datetime.datetime(2016, 2, 1, 6, 15, 37, 52428, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='probationer',
            name='name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
