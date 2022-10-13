
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import District, Company, Category, CompanyNetwork, Product
from .serializer import (ProductSerializer,
                         ProductDetailSerializer,
                         DistrictSerializer,
                         CompanySerializer,
                         CategorySerializer,
                         CompanyNetworkSerializer, )


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        product = get_object_or_404(self.queryset, pk=pk)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if 'id' in kwargs:
            self.queryset = self.queryset.filter(id=kwargs['id'])

        if district_id := request.query_params.get('district_id'):
            self.queryset = self.queryset.filter(district=district_id)

        context = {'district_id': request.query_params.get('district_id'),
                   'price': request.query_params.get('price'),
                   'category': request.query_params.get('category'),
                   'product_name': request.query_params.get('product_name')}

        serializer = self.serializer_class(self.queryset, many=True, context=context)

        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class CompanyNetworkViewSet(viewsets.ModelViewSet):
    queryset = CompanyNetwork.objects.all()
    serializer_class = CompanyNetworkSerializer
    permission_classes = [IsAuthenticated]
