# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-27 19:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0003_auto_20171217_2028'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Language')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='languages',
        ),
        migrations.AlterUniqueTogether(
            name='userlanguage',
            unique_together=set([('user_id', 'language_id')]),
        ),
    ]