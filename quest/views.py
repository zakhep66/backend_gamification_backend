from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from quest.models import Quest, QuestType
from quest.serializers import QuestSerializer, QuestTypeSerializer
from users.permissions import IsEmployee
from users.user_views import CustomAuthentication


class QuestViewSet(
	mixins.CreateModelMixin,
	mixins.UpdateModelMixin,
	mixins.RetrieveModelMixin,
	mixins.ListModelMixin,
	viewsets.GenericViewSet
):
	queryset = Quest.objects.all()
	serializer_class = QuestSerializer
	permission_classes = [IsAuthenticated, ]
	authentication_classes = [CustomAuthentication, ]

	def get_permissions(self):
		"""
		Определение прав доступа
		"""

		permission_classes = [IsEmployee, ] if self.action in ['create', 'update', 'partial_update', ] \
			else self.permission_classes
		return [permission() for permission in permission_classes]

	def create(self, request, *args, **kwargs):
		request.data['employee_id'] = request.user.id
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

	def partial_update(self, request, *args, **kwargs):
		# todo нужно обработать завершение квеста
		quest = self.get_object()

		if request.data.get('is_active', None) is False:
			comleted_quest()

		serializer = self.get_serializer(quest, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)

		return Response(serializer.data, status=status.HTTP_200_OK)


class QuestTypeViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = QuestType.objects.all()
	serializer_class = QuestTypeSerializer
	permission_classes = [IsAuthenticated, ]
	authentication_classes = [CustomAuthentication, ]
