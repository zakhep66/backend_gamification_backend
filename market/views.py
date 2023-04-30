from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from market.models import StoreProduct, StoreHistory
from market.serializers import StoreProductSerializer, StoreHistorySerializer
from market.services import MarketHandler
from transfer.permissions import IsStudent
from users.user_views import CustomAuthentication


class StoreProductViewSet(viewsets.ModelViewSet):
    queryset = StoreProduct.objects.all()
    serializer_class = StoreProductSerializer
    authentication_classes = [CustomAuthentication, ]

    def get_permissions(self):
        """
        Определяем права доступа к методам.
        """

        permission_classes = [IsAuthenticated, ] if self.action in ['list', ] else self.permission_classes
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, ])
    def all_student_product(self, request):
        return Response(
            *MarketHandler.get_all_student_buy(request.user.id)
        )


class StoreHistoryViewSet(viewsets.ModelViewSet):
    queryset = StoreHistory.objects.all()
    serializer_class = StoreHistorySerializer
    authentication_classes = [CustomAuthentication, ]

    @action(detail=False, methods=['post'], permission_classes=[IsStudent, ])
    def market_shop(self, request):
        return Response(
            *MarketHandler.make_shop(student_id=request.user.id, product_id=request.data.get('product_id'))
        )
