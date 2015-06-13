# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe', '0003_subscriptionlinks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionlinks',
            name='date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
