# Generated by Django 4.2.6 on 2023-10-20 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_products_series'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='image_link',
            field=models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Ссылка на фото'),
        ),
    ]
