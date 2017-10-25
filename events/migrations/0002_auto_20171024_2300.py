# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-24 23:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=300)),
                ('place_id', models.CharField(max_length=300, unique=True)),
                ('image', models.CharField(max_length=300, null=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('timezone', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='events.Category'),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='events.Location'),
        ),
    ]
