from django.db import models
from django.utils.text import slugify

from mptt.models import MPTTModel, TreeForeignKey

from base.utils import translit_to_eng


class Category(MPTTModel):
    name = models.CharField('Название', max_length=255)
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


class Brand(MPTTModel):
    name = models.CharField('Название', max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='slug', blank=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Родитель'
    )

    class MPTTMeta:
        """ Сортировка по вложенности """
        order_insertion_by = ('name',)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = f'{slugify(translit_to_eng(self.name))}'
        super().save(*args, **kwargs)


