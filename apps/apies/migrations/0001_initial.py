# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Api',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.IntegerField(verbose_name=b'Key ID')),
                ('vcode', models.CharField(max_length=254, verbose_name=b'Verification Code')),
                ('category', models.CharField(max_length=254)),
                ('expires', models.CharField(max_length=254, blank=True)),
                ('walletTransactions', models.NullBooleanField(default=None)),
                ('walletJournal', models.NullBooleanField(default=None)),
                ('marketOrders', models.NullBooleanField(default=None)),
                ('accountBalance', models.NullBooleanField(default=None)),
                ('notificationTexts', models.NullBooleanField(default=None)),
                ('notifications', models.NullBooleanField(default=None)),
                ('mailMessages', models.NullBooleanField(default=None)),
                ('mailingLists', models.NullBooleanField(default=None)),
                ('mailBodies', models.NullBooleanField(default=None)),
                ('contactNotifications', models.NullBooleanField(default=None)),
                ('contactList', models.NullBooleanField(default=None)),
                ('locations', models.NullBooleanField(default=None)),
                ('contracts', models.NullBooleanField(default=None)),
                ('accountStatus', models.NullBooleanField(default=None)),
                ('characterInfo', models.NullBooleanField(default=None)),
                ('upcomingCalendarEvents', models.NullBooleanField(default=None)),
                ('skillQueue', models.NullBooleanField(default=None)),
                ('skillInTraining', models.NullBooleanField(default=None)),
                ('characterSheet', models.NullBooleanField(default=None)),
                ('calendatEventAttendees', models.NullBooleanField(default=None)),
                ('assetList', models.NullBooleanField(default=None)),
                ('standings', models.NullBooleanField(default=None)),
                ('medals', models.NullBooleanField(default=None)),
                ('killLog', models.NullBooleanField(default=None)),
                ('facWarStats', models.NullBooleanField(default=None)),
                ('research', models.NullBooleanField(default=None)),
                ('industryJobs', models.NullBooleanField(default=None)),
                ('corp_killLog', models.NullBooleanField(default=None)),
                ('corp_memberTracking', models.NullBooleanField(default=None)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='api',
            unique_together=set([('key', 'vcode', 'user')]),
        ),
    ]
