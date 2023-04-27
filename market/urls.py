from django.urls import path, include
from rest_framework.routers import DefaultRouter

from market.views import StoreProductViewSet

router = DefaultRouter()
router.register(r'store_product', StoreProductViewSet, basename='store_product')
all_student_product = StoreProductViewSet.as_view({'get': 'all_student_product'}, basename='all_student_product')

urlpatterns = [
    path('', include(router.urls)),
    path('store_product/all_student_product', all_student_product, name='all_student_product')
]
