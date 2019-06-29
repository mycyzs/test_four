# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0003_auto_20190629_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='when_created',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
