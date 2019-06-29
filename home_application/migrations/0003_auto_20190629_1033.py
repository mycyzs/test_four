# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0002_auto_20190629_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='phone',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='title',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='when_created',
            field=models.DateTimeField(max_length=50, null=True),
        ),
    ]
