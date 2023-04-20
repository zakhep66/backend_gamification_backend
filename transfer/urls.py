from django.urls import path, include
from rest_framework.routers import DefaultRouter

from transfer.views import TransactionViewSet

router = DefaultRouter()
router.register(r'transaction', TransactionViewSet, basename='transaction')
transfer = TransactionViewSet.as_view({'post': 'transfer'})

urlpatterns = [
    path('', include(router.urls)),
    path('transaction/transfer/', transfer, name='transfer'),
]
