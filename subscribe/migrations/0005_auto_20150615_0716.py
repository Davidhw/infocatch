# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe', '0004_auto_20150610_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionlinks',
            name='links',
            field=models.CharField(max_length=4000),
        ),
    ]
