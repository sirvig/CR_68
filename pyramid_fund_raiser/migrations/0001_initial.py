# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Center',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('reference', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.CharField(max_length=10)),
                ('dt_donated', models.DateTimeField()),
                ('anon', models.BooleanField()),
                ('frequency', models.CharField(max_length=1, choices=[(b'1', b'One-time'), (b'2', b'Monthly')])),
                ('key', models.CharField(max_length=20)),
                ('confirmed', models.BooleanField()),
                ('center', models.ForeignKey(to='pyramid_fund_raiser.Center')),
            ],
            options={
                'ordering': ['-dt_donated'],
            },
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='donation',
            name='donor',
            field=models.ForeignKey(to='pyramid_fund_raiser.Donor'),
        ),
    ]
