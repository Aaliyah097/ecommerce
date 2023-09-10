from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey


class Currencies(models.Model):
    name = models.CharField(verbose_name='Название',
                            max_length=4,
                            unique=True)
    symbol = models.CharField(verbose_name='Символ',
                              max_length=1)

    def __str__(self):
        return f"{self.name} {self.symbol}"

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'
        db_table = 'currencies'


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


class Categories(MPTTModel):
    name = models.CharField(verbose_name='Название',
                            max_length=50)
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
    file = models.ImageField(verbose_name='Лого',
                             upload_to='categories/',
                             null=True,
                             blank=True)

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


@receiver(post_delete, sender=Categories)
def delete_categories_file(sender, instance, **kwargs):
    try:
        instance.file.delete(False)
    except AttributeError:
        pass


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
    description = models.TextField(verbose_name='Описание',
                                   default=None, blank=True, null=True)

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
    currency = models.ForeignKey(Currencies,
                                 verbose_name='Валюта',
                                 to_field='name',
                                 on_delete=models.SET_NULL,
                                 related_name='products_by_currency',
                                 null=True)
    description = models.TextField(verbose_name='Описание',
                                   default=None,
                                   blank=True,
                                   null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        db_table = 'products'
        ordering = ('-id', )

        unique_together = ('part_number', 'brand')


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
    value = models.TextField(verbose_name='Значение',
                             null=True)

    def __str__(self):
        return self.value

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


class Orders(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('finished', 'Завершенный'),
        ('estimating', 'Оценивается'),
        ('awaiting', 'Ожидает'),
        ('delivering', 'Доставляется'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменен'),
        ('payment', 'Ожидает оплаты'),
        ('payed', 'Оплачен'),
    )
    comment = models.TextField(verbose_name='Комментарий',
                               blank=True,
                               null=True,
                               default=None)
    status = models.CharField(verbose_name='Статус',
                              max_length=25,
                              choices=STATUS_CHOICES,
                              default='new')
    created_at = models.DateTimeField(verbose_name='Дата создания',
                                      auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления',
                                      auto_now=True)
    discount = models.FloatField(verbose_name='Скидка',
                                 default=0)
    client = models.TextField(verbose_name='Контакты',
                              default=None,
                              blank=True,
                              null=True)
    rate = models.FloatField(verbose_name='Курс к ₽',
                             default=None,
                             blank=True,
                             null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        db_table = 'orders'


class OrderItems(models.Model):
    order = models.ForeignKey(Orders,
                              verbose_name='Заказ',
                              related_name='order_items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Products,
                                verbose_name='Товар',
                                related_name='product_items',
                                on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Количество',
                                 default=0)
    comment = models.TextField(verbose_name='Комментарий',
                               default=None,
                               blank=True,
                               null=True)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'
        db_table = 'order_items'
