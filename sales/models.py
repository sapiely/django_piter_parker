from django.db import models
from django.db.models import Max, Min


class District(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'District'
        verbose_name_plural = 'Districts'


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class CompanyNetwork(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company Network'
        verbose_name_plural = 'Company Networks'


class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    district = models.ManyToManyField('District', related_name='companies')
    products = models.ManyToManyField('Product', through='CompanyProduct')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class CompanyProduct(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.company.name} {self.product.name} {self.price} Category: {self.product.category.name}'

    class Meta:
        verbose_name = 'Company Product'
        verbose_name_plural = 'Company Products'
