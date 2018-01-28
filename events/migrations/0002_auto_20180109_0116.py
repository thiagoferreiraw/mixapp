# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-01-09 01:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description_ar',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='description_de',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='description_en',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='description_es',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='description_fr',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='description_hi',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='description_it',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='description_ja',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='description_ko',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='description_nl',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='description_pt',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='description_pt_br',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='description_ru',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ar',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_de',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_es',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_fr',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_hi',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_it',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ja',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ko',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_nl',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_pt',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_pt_br',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ru',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='description_ar',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='description_de',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='description_en',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='description_es',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='description_fr',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='description_hi',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='description_it',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='description_ja',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='description_ko',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='description_nl',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='description_pt',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='description_pt_br',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='description_ru',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='name_ar',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='name_de',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='name_en',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='name_es',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='name_fr',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='name_hi',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='name_it',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='name_ja',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='name_ko',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='name_nl',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='name_pt',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='name_pt_br',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='name_ru',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
