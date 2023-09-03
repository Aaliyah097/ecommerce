from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey


class Categories(MPTTModel):
    name = models.CharField(verbose_name='Название',
                            max_length=50,
                            unique=True)
    slug = models.SlugField(verbose_name='Путь',
                            max_length=50,
                            primary_key=True,
                            unique=True,
                            null=False,)
    parent: 'Categories' = TreeForeignKey('self',
                                          verbose_name='Родитель',
                                          on_delete=models.SET_NULL,
                                          related_name='children',
                                          null=True, blank=True)

    def get_absolute_url(self):
        return reverse('catalog:categories-detail', kwargs={'pk': self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug_path = [self.slug]

        current_parent = self.parent
        while current_parent:
            slug_path.insert(0, current_parent.slug)
            current_parent = current_parent.parent

        self.slug = '-'.join(slug_path)

        super(Categories, self).save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'categories'
        unique_together = ('name', 'parent')


class Brands(models.Model):
    name = models.CharField(verbose_name='Название',
                            max_length=50,
                            unique=True)
    slug = models.SlugField(verbose_name='Путь',
                            max_length=50,
                            unique=True,
                            primary_key=True)
    file = models.ImageField(verbose_name='Фото',
                             upload_to='brands/',
                             null=True,
                             blank=True)

    def get_absolute_url(self):
        return reverse('catalog:brands-detail', kwargs={'pk': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'
        db_table = 'brands'


@receiver(post_delete, sender=Brands)
def delete_brand_file(sender, instance, **kwargs):
    try:
        instance.file.delete(False)
    except AttributeError:
        pass


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
                              verbose_name='Производитель',
                              null=True,
                              on_delete=models.SET_NULL,
                              related_name='products_by_brand')
    price = models.FloatField(verbose_name='Цена',
                              default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        db_table = 'products'

        unique_together = ('part_number', 'brand')


class Details(models.Model):
    name = models.CharField(verbose_name='Название',
                            max_length=50,
                            unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Свойство'
        verbose_name_plural = 'Свойства'
        db_table = 'details'


class Specs(models.Model):
    detail = models.ForeignKey(Details,
                               verbose_name='Характеристика',
                               on_delete=models.CASCADE,
                               related_name='in_specs_as_detail')
    product = models.ForeignKey(Products,
                                verbose_name='Товар',
                                on_delete=models.CASCADE,
                                related_name='specs',
                                null=True, default=None)
    value = models.TextField(verbose_name='Значение', null=True)

    def __str__(self):
        return f"{self.detail}: {self.value}"

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
        db_table = 'specs'
        unique_together = ('product', 'detail')


class Images(models.Model):
    product = models.ForeignKey(Products,
                                verbose_name='Товар',
                                on_delete=models.CASCADE,
                                related_name='images')
    file = models.ImageField(verbose_name='Фото',
                             upload_to='photos/')

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        db_table = 'images'


@receiver(post_delete, sender=Images)
def delete_image_file(sender, instance, **kwargs):
    try:
        instance.file.delete(False)
    except AttributeError:
        pass
