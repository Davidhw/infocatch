# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userSettings', '0003_auto_20150604_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='feed_Format',
            field=models.CharField(default=b'b', max_length=1, choices=[(b'b', b'Email List of All The Links'), (b'i', b'Email Individual Links'), (b'p', b"Email PDF Compilation of the Links' Content"), (b'e', b"Email EPUB Compilation of the Links' Content"), (b'r', b"Don't Email Links. (They'll still be available via RSS)")]),
        ),
    ]
