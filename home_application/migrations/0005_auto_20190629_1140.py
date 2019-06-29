# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0004_auto_20190629_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='comment',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='depart',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='result',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='score',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
