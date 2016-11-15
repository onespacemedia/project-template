# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import cms.apps.media.models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0003_file_alt_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Name of the setting', max_length=1024)),
                ('key', models.CharField(help_text=b'The key used to reference the setting', max_length=1024)),
                ('type', models.CharField(max_length=1024, choices=[(b'string', b'String'), (b'text', b'Text'), (b'number', b'Number'), (b'image', b'Image')])),
                ('string', models.CharField(max_length=2048, null=True, blank=True)),
                ('text', models.TextField(null=True, blank=True)),
                ('number', models.IntegerField(null=True, blank=True)),
                ('image', cms.apps.media.models.ImageRefField(related_name='+', on_delete=django.db.models.deletion.PROTECT, blank=True, to='media.File', null=True)),
            ],
        ),
    ]
