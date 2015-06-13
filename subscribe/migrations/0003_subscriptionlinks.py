# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe', '0002_subscriptionuserpairing'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionLinks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('links', models.CharField(max_length=800)),
                ('date', models.DateField()),
                ('subscription', models.ForeignKey(to='subscribe.Subscription')),
            ],
        ),
    ]
