from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from transfer.models import Transaction
from transfer.serializers import TransactionSerializer
from users.user_views import CustomAuthentication


class TransactionViewSet(viewsets.ModelViewSet):
	queryset = Transaction.objects.all()
	serializer_class = TransactionSerializer
	permission_classes = [IsAdminUser, ]
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

