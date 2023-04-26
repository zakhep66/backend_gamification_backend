from django.db import models

from users.models import BankAccount


class Transaction(models.Model):
	TRANSFER_TYPE = (
		('transfer', 'перевод'),
		('buy', 'покупка'),
		('achievement', 'ачивка')
	)

	bank_id_sender = models.ForeignKey(BankAccount, on_delete=models.DO_NOTHING, related_name='sender')
	bank_id_recipient = models.ForeignKey(BankAccount, on_delete=models.DO_NOTHING, related_name='recipient')
	comment = models.CharField(max_length=100)
	sum_count = models.PositiveIntegerField()
	date_time = models.DateTimeField(auto_now_add=True)
	transfer_type = models.CharField(choices=TRANSFER_TYPE, max_length=50)

	class Meta:
		verbose_name = 'Перевод'
		verbose_name_plural = 'Переводы'

	def __str__(self):
		return self.transfer_type
