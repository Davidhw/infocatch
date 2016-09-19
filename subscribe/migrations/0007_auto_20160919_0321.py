# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe', '0006_auto_20160919_0311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='url',
            field=models.CharField(max_length=300),
        ),
    ]
