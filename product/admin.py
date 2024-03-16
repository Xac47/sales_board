from django.contrib import admin
from django import forms
from mptt.admin import DraggableMPTTAdmin
from mptt.forms import TreeNodeChoiceField
from .models import Category, Brand, Product, BrandModel


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'id', 'name', 'slug')
    list_display_links = ('name', 'slug', 'id', 'indented_title')

    fieldsets = (
        ('Основная информация', {'fields': ('name', 'slug', 'parent')}),
    )


class BrandModelInline(admin.TabularInline):
    model = BrandModel


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name', 'slug')
    inlines = (BrandModelInline,)


@admin.register(BrandModel)
class BrandModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'model_name', 'slug')
    list_display_links = ('id', 'brand', 'model_name', 'slug')


class ProductAdminForm(forms.ModelForm):
    category = TreeNodeChoiceField(queryset=Category.objects.all(), empty_label='Выберите категорию')
    # brand = forms.ModelChoiceField(queryset=Brand.objects.all(), empty_label='Выберите бренд')

    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), empty_label='Выберите бренд',
                                   widget=forms.Select(attrs={'onchange': 'load_brand_models();', 'id': 'id_brand'}))

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'brand_model': forms.Select(attrs={'id': 'id_brand_model'}),
        }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'desc', 'price', 'category', 'brand')
    list_display_links = ('id', 'desc')

    form = ProductAdminForm
