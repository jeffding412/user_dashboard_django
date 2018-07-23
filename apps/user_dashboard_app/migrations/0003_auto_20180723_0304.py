# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-23 03:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_dashboard_app', '0002_auto_20180719_0445'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='display_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='post',
            name='receiver',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='wall_posts', to='user_dashboard_app.User'),
            preserve_default=False,
        ),
    ]
