# from celery import shared_task
# from django.db.transaction import atomic
# from rest_framework.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _
#
# from users.models import BankAccount
#
#
# @atomic
# @shared_task
# def process_transaction(from_id, to_id, sum_count, t_type, comment):
# 	from transfer.models import Transaction
# 	# Celery задача для обработки транзакции
# 	try:
# 		# Выполняем обработку транзакции, например, проводим перевод между счетами
# 		transaction_processed = False
# 		main_bank_account = BankAccount.objects.get(id=1)
# 		from_account, to_account = BankAccount.objects.get(id=from_id), BankAccount.objects.get(id=to_id)
#
# 		if t_type == 'transfer':
# 			# Если тип транзакции - перевод, списываем сумму с баланса отправителя и пополняем баланс получателя
# 			if from_account.balance >= sum_count:
# 				from_account.balance -= sum_count
# 				to_account.balance += sum_count
# 				from_account.save()
# 				to_account.save()
# 				transaction_processed = True
#
# 				Transaction.objects.create(
# 					from_id=from_id,
# 					to_id=to_id,
# 					comment=comment,
# 					sum_count=sum_count,
# 					transfer_type=t_type
# 				)
# 			else:
# 				raise ValidationError(_('Недостаточно средств на счете отправителя'))
# 		elif t_type == 'buy':
# 			# Если тип транзакции - покупка, списываем сумму с баланса отправителя
# 			if from_account.balance >= sum_count:
# 				from_account.balance -= sum_count
# 				main_bank_account.balance += sum_count
# 				from_account.save()
# 				main_bank_account.save()
# 				transaction_processed = True
# 			else:
# 				raise ValidationError(_('Недостаточно средств на счете отправителя'))
# 		elif t_type == 'achievement':
# 			# Если тип транзакции - ачивка, пополняем баланс получателя
# 			if main_bank_account.balance >= sum_count:
# 				to_account.balance += sum_count
# 				main_bank_account.balance -= sum_count
# 				to_account.save()
# 				main_bank_account.save()
# 				transaction_processed = True
# 		else:
# 			raise ValidationError(_('Неверный тип транзакции'))
#
# 	except Transaction.DoesNotExist:
# 		transaction_processed = False
# 	except Exception as e:
# 		# Обрабатываем ошибки при обработке транзакции, если необходимо
# 		transaction_processed = False
# 		print(f"Ошибка перевода между аккаунтами {from_id} и {to_id}: {e}")
#
# 	if transaction_processed:
# 		# Если транзакция успешно обработана, можно выполнить дополнительные действия, если необходимо
# 		# Например, отправить уведомление, записать в журнал и т.д.
# 		print('уведомление о переводе')
# 		pass
