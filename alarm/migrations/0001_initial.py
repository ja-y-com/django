# Generated by Django 4.0.4 on 2022-05-06 05:06

import core.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlarmStockClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='의뢰인')),
                ('phone_number', core.fields.PhoneNumberField(blank=True, max_length=15, null=True, verbose_name='휴대폰 번호')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='이메일 주소')),
            ],
            options={
                'verbose_name': '알람 의뢰인',
                'verbose_name_plural': '알람 의뢰인',
                'db_table': 'alarm_stock_client',
            },
        ),
        migrations.CreateModel(
            name='AlarmStockCos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='제품 링크')),
                ('option', models.CharField(blank=True, max_length=50, null=True, verbose_name='옵션')),
                ('is_enabled', models.BooleanField(default=True, verbose_name='사용 여부')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alarm.alarmstockclient', verbose_name='의뢰인')),
            ],
            options={
                'verbose_name': '재고 알람 - 코스',
                'verbose_name_plural': '재고 알람 - 코스',
                'db_table': 'alarm_stock_cos',
            },
        ),
    ]
