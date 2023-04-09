from rest_framework import viewsets

from .models import Direction
from .serializers import DirectionSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

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
