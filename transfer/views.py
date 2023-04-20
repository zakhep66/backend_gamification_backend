from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from transfer.models import Transaction
from transfer.serializers import TransactionSerializer
from users.models import BankAccount
from users.user_views import CustomAuthentication
from .tasks import process_transaction


class TransactionViewSet(viewsets.ModelViewSet):
	queryset = Transaction.objects.all()
	serializer_class = TransactionSerializer
	permission_classes = [IsAuthenticated, ]
	authentication_classes = [CustomAuthentication, ]

	def get_permissions(self):
		"""
		Определяем права доступа к методам.
		"""

		if self.action in ['list', 'retrieve']:
			permission_classes = [IsAuthenticated, ]
		else:
			permission_classes = self.permission_classes
		return [permission() for permission in permission_classes]

	@action(detail=False, methods=['post'])
	def transfer(self, request):
		# Получаем данные о транзакции из запроса
		from_account_id = request.data.get('from_id')
		to_account_id = request.data.get('to_id')
		sum_count = request.data.get('sum_count')
		comment = request.data.get('comment')
		transfer_type = request.data.get('transfer_type')

		try:
			# Проверяем наличие счетов отправителя и получателя
			# Запускаем Celery задачу для асинхронной обработки транзакции
			process_transaction.delay(from_account_id, to_account_id, sum_count, transfer_type, comment)

			return Response({'detail': 'Транзакция успешно создана'}, status=status.HTTP_201_CREATED)

		except BankAccount.DoesNotExist:
			return Response({'detail': 'Один из указанных счетов не существует'}, status=status.HTTP_400_BAD_REQUEST)

		except ValidationError as e:
			return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			return Response({'detail': 'Произошла ошибка при создании транзакции'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
