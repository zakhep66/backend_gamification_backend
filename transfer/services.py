import os

from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from market.models import StoreProduct, StoreHistory
from users.models import Student, BankAccount
from .models import Transaction


class TransactionHandler:
	MAIN_BANK_ACCOUNT_ID = int(os.environ.get('MAIN_BANK_ACCOUNT_ID'))
	TumoAccount = 'Tumo account'
	TumoComment = ''

	@staticmethod
	@transaction.atomic()
	def transfer_student_to_student(
			sender_id: int,
			recipient_id: int,
			amount: int,
			comment: str = '') -> tuple:
		transfer_type = 'transfer'
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
	def quest_transaction(student_id: Student, award_sum: int):
		transfer_type = 'quest'
		try:
			sender_account = BankAccount.objects.get(id=TransactionHandler.MAIN_BANK_ACCOUNT_ID)
			recipient_account = BankAccount.objects.get(student=student_id)

			if sender_account.balance < award_sum:
				error_message = 'Вы обанкротили Тумо. Недостаточно средств'
				raise ValidationError(error_message)

			sender_account.balance -= award_sum
			recipient_account.balance += award_sum
			sender_account.save()
			recipient_account.save()

		except BankAccount.DoesNotExist:
			error_message = 'Не найден банковский аккаунт'
			return str(Exception(error_message)), status.HTTP_400_BAD_REQUEST

		Transaction.objects.create(
			bank_id_sender=sender_account,
			bank_id_recipient=recipient_account,
			sum_count=award_sum,
			transfer_type=transfer_type,
			comment='Награда за выполнение квеста'
		)
		return {'detail': 'Награда зачислена'}, status.HTTP_200_OK

	@staticmethod
	@transaction.atomic()
	def market_transaction(sender_id: int, product_id) -> tuple:
		transfer_type = 'buy'
		try:
			product = StoreProduct.objects.get(id=product_id)
		except StoreProduct.DoesNotExist:
			raise Exception('Товар не найден')
		try:
			sender_account = Student.objects.get(id=sender_id).bank_account_id
			main_bank_account = BankAccount.objects.get(id=TransactionHandler.MAIN_BANK_ACCOUNT_ID)
		except Student.DoesNotExist:
			raise Exception('Пользователь не найден')
		except BankAccount.DoesNotExist:
			raise Exception('Не найден главный банковский аккаунт')

		if not sender_account.is_active:
			raise Exception('Ваш счёт заблокирован')
		elif sender_account.balance < product.price:
			raise Exception('Недостаточно средств на счёте')

		sender_account.balance -= product.price
		main_bank_account.balance += product.price
		sender_account.save()
		main_bank_account.save()

		Transaction.objects.create(
			bank_id_sender=sender_account,
			bank_id_recipient=main_bank_account,
			sum_count=product.price,
			transfer_type=transfer_type,
			comment=str(product.name)
		)

		StoreHistory.objects.create(
			store_product_id=product,
			buyer_bank_account_id=sender_account
		)
		return {'detail': 'Покупка прошла успешно'}, status.HTTP_201_CREATED

	@staticmethod
	def _transaction_response(t_qs):
		return [{
			'id': t.id,
			'sum_count': t.sum_count,
			'transfer_type': t.transfer_type,
			'comment': t.comment,
			'sender': {
				'id': t.bank_id_sender.student.id if hasattr(
					t.bank_id_sender, 'student') else TransactionHandler.MAIN_BANK_ACCOUNT_ID,
				'first_name': t.bank_id_sender.student.first_name if hasattr(
					t.bank_id_sender, 'student') else TransactionHandler.TumoAccount,
				'last_name': t.bank_id_sender.student.last_name if hasattr(
					t.bank_id_sender, 'student') else TransactionHandler.TumoComment,
			},
			'recipient': {
				'id': t.bank_id_recipient.student.id if hasattr(
					t.bank_id_recipient, 'student') else TransactionHandler.MAIN_BANK_ACCOUNT_ID,
				'first_name': t.bank_id_recipient.student.first_name if hasattr(
					t.bank_id_recipient, 'student') else TransactionHandler.TumoAccount,
				'last_name': t.bank_id_recipient.student.last_name if hasattr(
					t.bank_id_recipient, 'student') else TransactionHandler.TumoComment,
			},
			'date_time': t.date_time
		} for t in t_qs]

	@staticmethod
	def get_all_transfers_from_student(student_id):
		try:
			student_bank_account_id = Student.objects.get(id=student_id).bank_account_id
			transaction_qs = Transaction.objects.select_related(
				'bank_id_sender__student', 'bank_id_recipient__student'
			).filter(
				Q(bank_id_sender=student_bank_account_id) | Q(bank_id_recipient=student_bank_account_id)
			).order_by('-date_time')

			return TransactionHandler._transaction_response(transaction_qs), status.HTTP_200_OK

		except Student.DoesNotExist:
			return {'detail': 'Пользователь не найден'}, status.HTTP_400_BAD_REQUEST

	@staticmethod
	def get_all_transfers(transfer_type):
		transaction_qs = Transaction.objects.prefetch_related(
			'bank_id_sender__student', 'bank_id_recipient__student'
		).filter(transfer_type=transfer_type).order_by('-date_time')

		if transaction_qs.exists():
			return TransactionHandler._transaction_response(transaction_qs), status.HTTP_200_OK
		else:
			return {'error': f"Не найден тип транзакции: '{transfer_type}'"}, status.HTTP_404_NOT_FOUND
