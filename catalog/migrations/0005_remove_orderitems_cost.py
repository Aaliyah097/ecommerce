# Generated by Django 4.2.4 on 2023-09-10 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_rename_orderitem_orderitems_rename_order_orders'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitems',
            name='cost',
        ),
    ]
