# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe', '0005_auto_20150615_0716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='xpath',
            field=models.CharField(max_length=500),
        ),
    ]
