# Generated by Django 4.2.6 on 2023-10-18 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_remove_orders_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='is_hidden',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Скрытая'),
        ),
    ]
