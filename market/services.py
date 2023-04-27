from rest_framework import status

from market.models import StoreHistory


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
            'store_product': sb.store_product_id.name,
            'date_time': sb.date_time,
            'content': sb.content,
            'status': sb.status
        } for sb in student_buy], status.HTTP_200_OK
