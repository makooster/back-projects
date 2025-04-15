# Generated by Django 5.1.6 on 2025-04-14 07:50

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='core.category')),
            ],
        ),
        migrations.CreateModel(
            name='FinanceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.today, verbose_name='Date')),
                ('status', models.CharField(choices=[('BUSINESS', 'Бизнес'), ('PERSONAL', 'Личное'), ('TAX', 'Налог')], default='BUSINESS', max_length=20)),
                ('type', models.CharField(choices=[('REPLENISHMENT', 'Пополнение'), ('WITHDRAW', 'Снятие')], default='REPLENISHMENT', max_length=20)),
                ('sum', models.PositiveBigIntegerField(blank=True, default=0)),
                ('comment', models.TextField(blank=True, max_length=1500, null=True)),
                ('subcategory', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='core.subcategory')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
