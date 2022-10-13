import contextlib

from django.db import transaction

from rest_framework import serializers

from .models import District, Company, Category, CompanyNetwork, Product, CompanyProduct


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CompanyNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyNetwork
        fields = '__all__'


class CompanyProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(source='product.category')
    name = serializers.CharField(source='product.name')

    class Meta:
        model = CompanyProduct
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category_id'] = data.pop('category')
        data.update({'category_name': instance.category.name})
        return data


class ProductDetailSerializer(ProductSerializer):
    companies = CompanyProductSerializer(many=True, source='companyproduct_set')


class CompanySerializer(serializers.ModelSerializer):
    district = DistrictSerializer(many=True)
    products = serializers.SerializerMethodField(method_name="get_products")

    class Meta:
        model = Company
        fields = '__all__'
        depth = 1

    def update(self, instance, validated_data):
        with transaction.atomic():
            with contextlib.suppress(KeyError):
                product = validated_data.pop('companyproduct_set')[0]

                data = {
                    'company': instance.pk,
                    'product': product['product'].pk,
                    'price': product['price']
                }

                company_product = CompanyProductSerializer(data=data)
                company_product.is_valid()
                company_product.save()

            super().update(instance, validated_data)

            return instance

    def get_products(self, obj):
        many = False

        products = CompanyProduct.objects.filter(company_id=obj.id).select_related()

        if category := self.context.get('category'):
            products = products.filter(product__category__name=category)
        if product_name := self.context.get('product_name'):
            products = products.filter(product__name__contains=product_name)

        ordering = self.context.get('price')
        if ordering == 'max':
            products = products.order_by('-price').first()
        elif ordering == 'min':
            products = products.order_by('price').first()
        else:
            products = products
            many = True

        if not products:
            return None

        return CompanyProductSerializer(products, many=many).data
