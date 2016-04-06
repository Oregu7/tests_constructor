# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0004_answer_analytics'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('translate', models.TextField()),
                ('image', models.ImageField(upload_to='images/')),
                ('test', models.ForeignKey(to='constructor.Test')),
            ],
        ),
    ]
