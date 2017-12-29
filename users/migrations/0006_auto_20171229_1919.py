# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-29 19:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20171227_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='actual_city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actual_city', to='events.City'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='birth_city', to='events.City'),
        ),
    ]
