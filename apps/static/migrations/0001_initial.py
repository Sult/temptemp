# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=254)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConquerableStation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stationID', models.IntegerField()),
                ('stationName', models.CharField(max_length=254)),
                ('stationTypeID', models.IntegerField()),
                ('solarSystemID', models.IntegerField()),
                ('corporationID', models.IntegerField()),
                ('corporationName', models.CharField(max_length=254)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RequiredSkill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('skillLevel', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('typeID', models.IntegerField(unique=True)),
                ('typeName', models.CharField(max_length=254)),
                ('published', models.IntegerField()),
                ('description', models.TextField()),
                ('rank', models.IntegerField()),
                ('primaryAttribute', models.ForeignKey(related_name='+', to='static.Attribute')),
                ('secondaryAttribute', models.ForeignKey(related_name='+', to='static.Attribute')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SkillBonus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bonusType', models.CharField(max_length=254)),
                ('bonusValue', models.FloatField()),
                ('skill', models.ForeignKey(to='static.Skill')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SkillGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('groupID', models.IntegerField()),
                ('groupName', models.CharField(unique=True, max_length=254)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WalletRefTypes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('refTypeID', models.IntegerField(unique=True)),
                ('refTypeName', models.CharField(max_length=254)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='skill',
            name='skillGroup',
            field=models.ForeignKey(to='static.SkillGroup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='requiredskill',
            name='required',
            field=models.ForeignKey(related_name='required', to='static.Skill'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='requiredskill',
            name='skill',
            field=models.ForeignKey(related_name='required_skills', to='static.Skill'),
            preserve_default=True,
        ),
    ]
