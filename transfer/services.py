from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from .models import Transaction, BankAccount


class TransactionHandler:
    @staticmethod
    @transaction.atomic()
    def make_transaction(from_account_id, to_account_id, amount, transfer_type, comment=''):
        try:
            from_account = BankAccount.objects.select_for_update().get(id=from_account_id)
            to_account = BankAccount.objects.select_for_update().get(id=to_account_id)
        except BankAccount.DoesNotExist:
            return {'detail': 'Указанный счёт не существует'}, status.HTTP_400_BAD_REQUEST

        if not from_account.is_active or not to_account.is_active:
            return {'detail': 'Один из счетов операции заблокирован'}, status.HTTP_400_BAD_REQUEST
        elif from_account == to_account:
            return {'detail': 'Нельзя произвести перевод самому себе'}, status.HTTP_400_BAD_REQUEST
        elif from_account.balance < amount:
            return {'detail': 'Недостаточно средств на счёте'}, status.HTTP_400_BAD_REQUEST

        from_account.balance -= amount
        to_account.balance += amount

        from_account.save()
        to_account.save()

        transaction = Transaction.objects.create(
            from_id=from_account,
            to_id=to_account,
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
