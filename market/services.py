from rest_framework import status

from market.models import StoreHistory, StoreProduct
from market.serializers import IssuedStoreHistorySerializer
from transfer.services import TransactionHandler
from achievement.tasks import CeleryAchievementTasks
from users.models import Student


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
        """
        Покупка товара в магазине
        """
        # Получаем объекты студента и товара
        try:
            student = Student.objects.get(id=student_id)
            product = StoreProduct.objects.get(id=product_id)
        except Student.DoesNotExist:
            return {'detail': 'Пользователь не найден'}, status.HTTP_400_BAD_REQUEST
        except StoreProduct.DoesNotExist:
            return {'detail': 'Товар не найден'}, status.HTTP_400_BAD_REQUEST

        # Проверяем, есть ли товар в наличии
        if not product.in_stock:
            return {'detail': 'Товар временно недоступен'}, status.HTTP_400_BAD_REQUEST

        # Проверяем, купил ли студент этот товар ранее
        if product.product_type != 'merch':
            already_bought = StoreHistory.objects.filter(
                store_product_id=product_id,
                buyer_bank_account_id=student.bank_account_id
            ).exists()
            if already_bought:
                return {'detail': 'Вы уже купили этот товар'}, status.HTTP_400_BAD_REQUEST

        try:
            shop = TransactionHandler.market_transaction(product_id=product_id, sender_id=student_id)
        except Exception as e:
            error_message = str(e)  # Получение сообщения об ошибке
            return {'detail': error_message}, status.HTTP_400_BAD_REQUEST

        # ачивка за первую покупку
        CeleryAchievementTasks.award_achievement_on_first_purchase.delay(student_id)

        return shop

    @staticmethod
    def get_all_non_issued_items():
        """
        Возвращает все не выданные товары типа merch
        """
        data_qs = StoreHistory.objects.select_related('store_product_id', 'buyer_bank_account_id__student').filter(
            status=False, store_product_id__product_type='merch'
        )
        serialized_data = IssuedStoreHistorySerializer(data_qs, many=True).data
        return serialized_data, status.HTTP_200_OK

    @staticmethod
    def get_opportunity_student_buy(student_id):
        return StoreProduct.get_available_products_for_student(student_id=student_id)
