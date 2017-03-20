# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GsmDevice',
            fields=[
                ('device_id', models.CharField(default='123456789', max_length=20, serialize=False, primary_key=True)),
                ('status', models.CharField(max_length=2, choices=[('A', 'active'), ('D', 'not active')])),
                ('activated_date', models.DateField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('gestation', models.IntegerField()),
                ('status', models.CharField(max_length=2, choices=[('A', 'active'), ('D', 'not active')])),
                ('gsm', models.ForeignKey(primary_key=True, serialize=False, to='Activity_Monitor.GsmDevice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Practitioner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=2, choices=[('A', 'assigned'), ('D', 'not assigned')])),
                ('pos', models.CharField(max_length=2, choices=[('D', 'doctor'), ('N', 'nurse')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SmsData',
            fields=[
                ('heart_rate', models.FloatField(default=0.0)),
                ('kick_count', models.FloatField(default=0.0)),
                ('date', models.DateTimeField(auto_now_add=True, serialize=False, primary_key=True)),
                ('gsm', models.ForeignKey(to='Activity_Monitor.GsmDevice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SystemUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('sex', models.CharField(max_length=2, choices=[('M', 'Male'), ('F', 'Female')])),
                ('birthday', models.DateField(blank=True)),
                ('age', models.IntegerField()),
                ('tel', models.CharField(max_length=14)),
                ('address', models.TextField()),
                ('reg_date', models.DateField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('hospitalID', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=30, unique=True, null=True)),
                ('email', models.EmailField(unique=True, max_length=75)),
                ('password', models.CharField(max_length=30)),
                ('salt', models.CharField(max_length=10)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('employee_agreement_file', models.FileField(upload_to='agreement_files', blank=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now_add=True)),
                ('SystemUser', models.ForeignKey(to='Activity_Monitor.SystemUser', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='practitioner',
            name='user',
            field=models.ForeignKey(to='Activity_Monitor.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='patient',
            name='SystemUser',
            field=models.ForeignKey(to='Activity_Monitor.SystemUser', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='patient',
            name='practitioner',
            field=models.ForeignKey(to='Activity_Monitor.Practitioner', null=True),
            preserve_default=True,
        ),
    ]
