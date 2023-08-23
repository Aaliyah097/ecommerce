from django.db import models

# Create your models here.


class Categories(models.Model):
    name = models.CharField(verbose_name='Название',
                            max_length=50)
    slug = models.SlugField(verbose_name='Путь',
                            max_length=50)
    parent = models.ForeignKey('Categories', verbose_name='Родитель',
                               on_delete=models.SET_NULL,
                               related_name='children',
                               null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'categories'
        unique_together = ('name', 'parent')


class Brands(models.Model):
    name = models.CharField(verbose_name='Название',
                            max_length=50,
                            unique=True,
                            primary_key=True)
    slug = models.SlugField(verbose_name='Путь',
                            max_length=50,
                            unique=True)

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'
        db_table = 'brands'


class Products(models.Model):
    name = models.CharField(verbose_name='Название',
                            max_length=500,
                            db_index=True)
    category = models.ForeignKey(Categories,
                                 null=True,
                                 verbose_name='Категория',
                                 on_delete=models.SET_NULL,
                                 related_name='products_by_category')
    part_number = models.CharField(verbose_name='Парт. номер',
                                   max_length=50,
                                   db_index=True)
    brand = models.ForeignKey(Brands,
                              to_field='name',
                              null=True,
                              verbose_name='Производитель',
                              on_delete=models.SET_NULL,
                              related_name='products_by_brand')
    price = models.FloatField(verbose_name='Цена',
                              default=0)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        db_table = 'products'

        unique_together = ('part_number', 'brand')


class Details(models.Model):
    name = models.CharField(verbose_name='Название',
                            max_length=50,
                            unique=True,
                            primary_key=True)

    class Meta:
        verbose_name = 'Свойство'
        verbose_name_plural = 'Свойства'
        db_table = 'details'


class ProductDetails(models.Model):
    detail = models.ForeignKey(Details,
                               to_field='name',
                               verbose_name='Характеристика',
                               on_delete=models.CASCADE,
                               related_name='in_products_as_detail')
    product = models.ForeignKey(Products,
                                verbose_name='Товар',
                                on_delete=models.CASCADE,
                                related_name='details')
    value = models.TextField(verbose_name='Значение', null=True)

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
        db_table = 'product_details'
        unique_together = ('product', 'detail')


class Images(models.Model):
    product = models.ForeignKey(Products,
                                verbose_name='Товар',
                                on_delete=models.CASCADE,
                                related_name='images')
    file = models.ImageField(verbose_name='Фото',
                             upload_to='photos/')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        db_table = 'images'
