from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from market.models import StoreProduct, StoreHistory
from market.serializers import StoreProductSerializer, StoreHistorySerializer
from market.services import MarketHandler
from transfer.permissions import IsStudent
from users.permissions import IsEmployeeManagerOrCouch
from users.user_views import CustomAuthentication


class StoreProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StoreProduct.objects.all()
    serializer_class = StoreProductSerializer
    authentication_classes = [CustomAuthentication, ]

    def get_permissions(self):
        """
        Определяем права доступа к методам.
        """

        permission_classes = [IsAuthenticated, ] if self.action in ['list', ] else self.permission_classes
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    # необязательный метод, пусть пока что будет
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, ])
    def all_student_product(self, request):
        """
        Возвращает все товары купленные студентом
        """
        return Response(
            *MarketHandler.get_all_student_buy(request.user.id)
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, ])
    def opportunity_student_buy(self, request):
        """
        Возвращает товары, которые может купить студент
        """
        student_id = request.user.id
        available_products = MarketHandler.get_opportunity_student_buy(student_id)
        serializer = StoreProductSerializer(available_products, many=True)
        return Response(serializer.data)


class StoreHistoryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = StoreHistory.objects.all()
    serializer_class = StoreHistorySerializer
    authentication_classes = [CustomAuthentication, ]

    def get_permissions(self):
        permission_classes = [IsEmployeeManagerOrCouch, ] if self.action == 'perform_update' \
            else self.permission_classes
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], permission_classes=[IsStudent, ])
    def market_shop(self, request):
        """
        Совершает покупку товара
        """
        return Response(
            *MarketHandler.make_shop(student_id=request.user.id, product_id=request.data.get('product_id'))
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, ])
    def all_non_issued_items(self, request):
        """
        Возвращает все не выданные товары типа merch
        """
        return Response(
            *MarketHandler.get_all_non_issued_items()
        )

    def partial_update(self, request, *args, **kwargs):
        """
        Изменяет статус выдачи товара типа merch на True
        принимает значение 'status' в теле запроса
        """
        store_history = self.get_object()

        if 'status' not in request.data:
            return Response({"detail": "Параметр 'status' отсутствует в запросе."}, status=status.HTTP_400_BAD_REQUEST)

        if store_history.store_product_id.product_type != 'merch':
            return Response({"detail": "Товар не является типом 'merch'."}, status=status.HTTP_400_BAD_REQUEST)

        store_history.status = request.data['status']
        store_history.save()

        return Response({"detail": "Статус истории товара успешно изменен."}, status=status.HTTP_200_OK)
