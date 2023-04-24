from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from users.models import Student, BankAccount
from .models import Transaction


class TransactionHandler:
    @staticmethod
    @transaction.atomic()
    def make_transaction(sender_id: int, recipient_id: int, amount: int, transfer_type: str, comment: str = ''):
        try:
            sender_account = Student.objects.get(id=sender_id).bank_account_id
            recipient_account = Student.objects.get(id=recipient_id).bank_account_id
        except Student.DoesNotExist:
            return {'detail': 'Пользователь не найден'}, status.HTTP_400_BAD_REQUEST

        if not sender_account.is_active or not recipient_account.is_active:
            return {'detail': 'Один из счетов операции заблокирован'}, status.HTTP_400_BAD_REQUEST
        elif sender_account.id == recipient_account.id:
            return {'detail': 'Нельзя произвести перевод самому себе'}, status.HTTP_400_BAD_REQUEST
        elif sender_account.balance < amount:
            return {'detail': 'Недостаточно средств на счёте'}, status.HTTP_400_BAD_REQUEST

        sender_account.balance -= amount
        recipient_account.balance += amount

        sender_account.save()
        recipient_account.save()

        transaction = Transaction.objects.create(
            from_id=sender_account,
            to_id=recipient_account,
            sum_count=amount,
            transfer_type=transfer_type,
            comment=comment
        )

        return {'detail': 'Транзакция успешно создана'}, status.HTTP_201_CREATED

    @staticmethod
    @transaction.atomic()
    def achievement_transaction(to_account_id, amount, comment, MAIN_BANK_ACCOUNT=1):
        to_account = BankAccount.objects.select_for_update().get(id=to_account_id)

        to_account.balance += amount
        to_account.save()

        transaction = Transaction.objects.create(
            from_id=MAIN_BANK_ACCOUNT,
            to_id=to_account_id,
            comment=comment,
            sum_count=amount,
            transfer_type="achievement"
        )

        return transaction.id

    @staticmethod
    @transaction.atomic()
    def market_transaction(to_account_id, amount, comment, MAIN_BANK_ACCOUNT=1):
        to_account = BankAccount.objects.select_for_update().get(id=to_account_id)

        to_account.balance -= amount
        to_account.save()

        transaction = Transaction.objects.create(
            from_id=MAIN_BANK_ACCOUNT,
            to_id=to_account_id,
            comment=comment,
            sum_count=amount,
            transfer_type="buy"
        )

        return transaction.id
