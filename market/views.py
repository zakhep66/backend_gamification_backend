from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from market.models import StoreProduct
from market.serializers import StoreProductSerializer
from market.services import MarketHandler
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
