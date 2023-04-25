from django.urls import path, include
from rest_framework.routers import DefaultRouter

from transfer.views import TransactionViewSet

router = DefaultRouter()
router.register(r'transaction', TransactionViewSet, basename='transaction')
transfer = TransactionViewSet.as_view({'post': 'transfer'})
all_student_transfer = TransactionViewSet.as_view({'get': 'all_student_transfer'})
all_transfers = TransactionViewSet.as_view({'get': 'all_transfers'})

urlpatterns = [
    path('', include(router.urls)),
    path('transaction/transfer/', transfer, name='transfer'),
    path('transaction/all_student_transfer', all_student_transfer, name='all_student_transfer'),
    path('transaction/all_transfers', all_transfers, name='all_transfers'),
]
