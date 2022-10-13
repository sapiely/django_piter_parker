from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import (ProductViewSet,
                    DistrictViewSet,
                    CompanyViewSet,
                    CategoryViewSet,
                    CompanyNetworkViewSet,)

router = DefaultRouter()
router.register('products', viewset=ProductViewSet, basename='product')
router.register('districts', viewset=DistrictViewSet, basename='district')
router.register('categories', viewset=CategoryViewSet, basename='category')
router.register('company_networks', viewset=CompanyNetworkViewSet, basename='company-network')


company_router = DefaultRouter()

company_detail = CompanyViewSet.as_view({
    "get": "list"
})


urlpatterns = [
    path('', include(router.urls)),
    path('organizations/', company_detail, name='organization-list'),
    path('organizations/<int:id>/', company_detail, name='organization-detail'),
    path('obtain-auth-token/', obtain_auth_token)
]
