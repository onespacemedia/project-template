# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('old_path', models.CharField(help_text=b"This should be an absolute path, excluding the domain name. Example: '/events/search/'.", unique=True, max_length=200, verbose_name=b'redirect from', db_index=True)),
                ('new_path', models.CharField(help_text=b"This can be either an absolute path (as above) or a full URL starting with 'http://'.", max_length=200, verbose_name=b'redirect to', blank=True)),
            ],
            options={
                'ordering': ('old_path',),
                'verbose_name': 'redirect',
                'verbose_name_plural': 'redirects',
            },
        ),
    ]
