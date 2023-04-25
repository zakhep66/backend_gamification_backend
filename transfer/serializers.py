from rest_framework import serializers

from transfer.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transaction
		fields = '__all__'
