# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-18 23:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_signupinvitation_invited_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignupWaitingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
