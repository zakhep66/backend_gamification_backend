from rest_framework import status
from rest_framework.response import Response

from market.models import StoreHistory, StoreProduct
from transfer.services import TransactionHandler


class MarketHandler:
    @staticmethod
    def get_all_student_buy(student_id):
        student_buy = StoreHistory.objects.select_related(
            'buyer_bank_account_id__student', 'store_product_id'
        ).filter(
            buyer_bank_account_id__student=student_id
        )
        return [{
            'id': sb.id,
            'store_product': {
                'id': sb.store_product_id.id,
                'name': sb.store_product_id.name,
                'description': sb.store_product_id.description,
                'image': sb.store_product_id.image.url,
                'product_type': sb.store_product_id.product_type
            },
            'date_time': sb.date_time,
            'content': sb.content,
            'status': sb.status
        } for sb in student_buy], status.HTTP_200_OK

    @staticmethod
    def make_shop(product_id: int, student_id: int):
        return TransactionHandler.market_transaction(product_id=product_id, sender_id=student_id)

    @staticmethod
    def get_all_non_issued_items():
        data_qs = StoreHistory.objects.select_related('store_product_id').filter(
            status=False, store_product_id__product_type='merch'
        )
        return data_qs, status.HTTP_200_OK

