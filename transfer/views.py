from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from transfer.models import Transaction
from transfer.serializers import TransactionSerializer
from users.models import BankAccount, Student
from users.user_views import CustomAuthentication
from .permissions import IsStudent
from .services import TransactionHandler
# from .tasks import process_transaction


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [CustomAuthentication, ]

    def get_permissions(self):
        """
        Определяем права доступа к методам.
        """

        permission_classes = [IsAuthenticated, ] if self.action in ['list', 'retrieve'] else self.permission_classes
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], permission_classes=[IsStudent, ])
    def transfer(self, request):
        return Response(
            *TransactionHandler.make_transaction(
                sender_id=request.user.id,
                recipient_id=request.data.get('to_id'),
                amount=request.data.get('sum_count'),
                transfer_type=request.data.get('transfer_type'),
                comment=request.data.get('comment')
            )
        )
