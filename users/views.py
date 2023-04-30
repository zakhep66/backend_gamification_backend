from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Direction, BankAccount
from .serializers import DirectionSerializer, BankAccountSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .servises import BankAccountHandler
from .user_views import CustomAuthentication


class DirectionViewSet(viewsets.ModelViewSet):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer
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


class BankAccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [CustomAuthentication, ]

    @action(detail=False, methods=['get'], permission_classes=permission_classes)
    def all_money_in_app(self, request):
        return Response(
            *BankAccountHandler.get_all_count_money()
        )
