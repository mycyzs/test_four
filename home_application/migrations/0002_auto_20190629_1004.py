# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='host',
            name='is_success',
        ),
        migrations.RemoveField(
            model_name='host',
            name='text',
        ),
        migrations.AddField(
            model_name='host',
            name='address',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='biz_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='owner',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='status',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='type',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
