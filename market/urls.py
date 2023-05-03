from django.urls import path, include
from rest_framework.routers import DefaultRouter

from market.views import StoreProductViewSet, StoreHistoryViewSet

router = DefaultRouter()
router.register(r'store_product', StoreProductViewSet, basename='store_product')
all_student_product = StoreProductViewSet.as_view({'get': 'all_student_product'}, basename='all_student_product')
market_shop = StoreHistoryViewSet.as_view({'post': 'market_shop'}, basename='market_shop')
all_non_issued_items = StoreHistoryViewSet.as_view({'get': 'all_non_issued_items'}, basename='all_non_issued_items')

urlpatterns = [
    path('', include(router.urls)),
    path('store_product/all_student_product', all_student_product, name='all_student_product'),
    path('store/market_shop', market_shop, name='market_shop'),
    path('store/all_non_issued_items', all_non_issued_items, name='all_non_issued_items'),
]
