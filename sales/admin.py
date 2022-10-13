from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import District, Company, Category, CompanyNetwork, Product, CompanyProduct


@admin.register(District)
class DistrictAdmin(ModelAdmin):
    list_display = ['name']
    sortable_by = ['name']
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name']
    sortable_by = ['name']
    search_fields = ['name']


@admin.register(CompanyNetwork)
class CompanyNetworkAdmin(ModelAdmin):
    list_display = ['name']
    sortable_by = ['name']
    search_fields = ['name']


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    list_display = ['name']
    sortable_by = ['name']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['name', 'product_category']
    sortable_by = ['name']
    search_fields = ['name']

    def product_category(self, obj):
        return obj.category.name


@admin.register(CompanyProduct)
class CompanyProductAdmin(ModelAdmin):
    list_display = ['company', 'product', 'price', 'product_category']
    list_filter = ['company', 'product']
    sortable_by = ['company', 'product', 'price']
    search_fields = ['company', 'product', 'price']

    def product_category(self, obj):
        return obj.product.category.name
