from rest_framework import viewsets, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response

from achievement.models import Achievement
from achievement.serializers import AchievementSerializer
from achievement.services import AchievementHandler
from transfer.permissions import IsStudent
from users.user_views import CustomAuthentication


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    authentication_classes = [CustomAuthentication, ]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(request.method)

    @action(detail=False, methods=['get'], permission_classes=[IsStudent, ])
    def student_achievement(self, request):
        return Response(
            *AchievementHandler.get_student_achievement(student_id=request.user.id)
        )
