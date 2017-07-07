# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redirects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='redirect',
            name='regular_expression',
            field=models.BooleanField(default=False, help_text=b"This will allow using regular expressions to match and replace patterns in URLs. See the <a href='https://docs.python.org/2/library/re.html' target='_blank'>Python regular expression documentation for details."),
        ),
        migrations.AddField(
            model_name='redirect',
            name='test_path',
            field=models.CharField(help_text=b'You will need to specify a test path to ensure your regular expression is valid.', max_length=200, null=True, blank=True),
        ),
    ]
