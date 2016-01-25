# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0006_auto_20160125_0833'),
    ]

    operations = [
        migrations.RenameField(
            model_name='query',
            old_name='helps',
            new_name='help',
        ),
    ]
