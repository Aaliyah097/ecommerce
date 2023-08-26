# Generated by Django 4.2.4 on 2023-08-26 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='Путь')),
                ('file', models.ImageField(blank=True, null=True, upload_to='brands/', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Производитель',
                'verbose_name_plural': 'Производители',
                'db_table': 'brands',
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('slug', models.SlugField(verbose_name='Путь')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='catalog.categories', verbose_name='Родитель')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'db_table': 'categories',
                'unique_together': {('name', 'parent')},
            },
        ),
        migrations.CreateModel(
            name='Details',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Свойство',
                'verbose_name_plural': 'Свойства',
                'db_table': 'details',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=500, verbose_name='Название')),
                ('part_number', models.CharField(db_index=True, max_length=50, verbose_name='Парт. номер')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products_by_brand', to='catalog.brands', verbose_name='Производитель')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products_by_category', to='catalog.categories', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'db_table': 'products',
                'unique_together': {('part_number', 'brand')},
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='photos/', verbose_name='Фото')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='catalog.products', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Фотография',
                'verbose_name_plural': 'Фотографии',
                'db_table': 'images',
            },
        ),
        migrations.CreateModel(
            name='Specs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(null=True, verbose_name='Значение')),
                ('detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_products_as_detail', to='catalog.details', verbose_name='Характеристика')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specs', to='catalog.products', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Характеристика',
                'verbose_name_plural': 'Характеристики',
                'db_table': 'specs',
                'unique_together': {('product', 'detail')},
            },
        ),
    ]
