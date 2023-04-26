from django.db import transaction
from django.db.models import Q
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
        elif amount <= 0:
            return {'detail': 'Нельзя переводить ноль или меньше'}, status.HTTP_400_BAD_REQUEST

        sender_account.balance -= amount
        recipient_account.balance += amount

        sender_account.save()
        recipient_account.save()

        Transaction.objects.create(
            bank_id_sender=sender_account,
            bank_id_recipient=recipient_account,
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

        # transaction = Transaction.objects.create(
        #     from_id=MAIN_BANK_ACCOUNT,
        #     to_id=to_account_id,
        #     comment=comment,
        #     sum_count=amount,
        #     transfer_type="achievement"
        # )

        # return transaction.id

    @staticmethod
    @transaction.atomic()
    def market_transaction(to_account_id, amount, comment, MAIN_BANK_ACCOUNT=1):
        to_account = BankAccount.objects.select_for_update().get(id=to_account_id)

        to_account.balance -= amount
        to_account.save()

        # transaction = Transaction.objects.create(
        #     from_id=MAIN_BANK_ACCOUNT,
        #     to_id=to_account_id,
        #     comment=comment,
        #     sum_count=amount,
        #     transfer_type="buy"
        # )
        #
        # return transaction.id

    @staticmethod
    def transaction_response(t_qs):
        return [{
            'id': t.id,
            'sum_count': t.sum_count,
            'transfer_type': t.transfer_type,
            'comment': t.comment,
            'sender': {
                'id': t.bank_id_sender.student.id,
                'first_name': t.bank_id_sender.student.first_name,
                'last_name': t.bank_id_sender.student.last_name,
            },
            'recipient': {
                'id': t.bank_id_recipient.student.id,
                'first_name': t.bank_id_recipient.student.first_name,
                'last_name': t.bank_id_recipient.student.last_name,
            },
            'date_time': t.date_time
        } for t in t_qs]

    @staticmethod
    def get_all_transfers_from_student(student_id):
        try:
            student_bank_account_id = Student.objects.get(id=student_id).bank_account_id
            transaction_qs = Transaction.objects.filter(
                Q(bank_id_sender=student_bank_account_id) | Q(bank_id_recipient=student_bank_account_id)
            ).select_related('bank_id_sender__student', 'bank_id_recipient__student').order_by('-date_time')

            return TransactionHandler.transaction_response(transaction_qs), status.HTTP_200_OK
        except Student.DoesNotExist:
            return {'detail': 'Пользователь не найден'}, status.HTTP_400_BAD_REQUEST

    @staticmethod
    def get_all_transfers(transfer_type):
        transaction_qs = Transaction.objects.filter(transfer_type=transfer_type).order_by('-date_time')
        return TransactionHandler.transaction_response(transaction_qs), status.HTTP_200_OK
