from django.db import models
from django.utils.text import slugify

from mptt.models import MPTTModel, TreeForeignKey

from base.utils import translit_to_eng


class Category(MPTTModel):
    name = models.CharField('Название', max_length=255, unique=True)
    slug = models.SlugField(max_length=255, verbose_name='slug', blank=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        """ Сортировка по вложенности """
        order_insertion_by = ('name',)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = f'{slugify(translit_to_eng(self.name))}'
        super().save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField('Название', max_length=255, unique=True)
    slug = models.SlugField(max_length=255, verbose_name='slug', blank=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = f'{slugify(translit_to_eng(self.name))}'
        super().save(*args, **kwargs)


class BrandModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Бренд', related_name='models_brand')
    model_name = models.CharField('Модель', max_length=255, unique=True)
    slug = models.SlugField(max_length=255, verbose_name='slug', blank=True)

    class Meta:
        verbose_name = 'Модель бренда'
        verbose_name_plural = 'Модели брендов'

    def __str__(self):
        return f'{self.brand} / {self.model_name}'

    def save(self, *args, **kwargs):
        self.slug = f'{self.brand.slug}__{slugify(translit_to_eng(self.model_name))}'
        super().save(*args, **kwargs)


class Product(models.Model):
    desc = models.TextField('Описание')
    slug = models.SlugField(max_length=255, verbose_name='slug', blank=True)
    price = models.DecimalField('Цена', decimal_places=2, max_digits=10)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Бренд')
    brand_model = models.ForeignKey(BrandModel, on_delete=models.CASCADE, verbose_name='Модель бренда')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.desc

    # def save(self, *args, **kwargs):
    #     self.slug = f'{slugify(translit_to_eng(self.name))}'
    #     super().save(*args, **kwargs)
