from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from quest.models import Quest, QuestType
from quest.serializers import QuestSerializer, QuestTypeSerializer
from quest.services import QuestHandler
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
		quest = self.get_object()

		if request.data.get('is_active', None) is False and quest.student_id is not None:
			try:
				QuestHandler.quest_completed(quest=quest)
			except Exception as e:
				error_message = str(e)
				error_response = {'detail': error_message}
				return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

		serializer = self.get_serializer(quest, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)

		return Response(serializer.data, status=status.HTTP_200_OK)

	@action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, ])
	def all_is_active_quest(self, request):
		"""
		Возвращает все активные квесты
		"""
		return Response(
			*QuestHandler.get_all_is_active()
		)

	@action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, ])
	def student_quest(self, request):
		return Response(
			*QuestHandler.get_student_quest(student_id=request.data.get('student_id'))
		)

	@action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, ])
	def employee_quest(self, request):
		return Response(
			*QuestHandler.get_employee_quest(employee_id=request.data.get('employee_id'))
		)


class QuestTypeViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = QuestType.objects.all()
	serializer_class = QuestTypeSerializer
	permission_classes = [IsAuthenticated, ]
	authentication_classes = [CustomAuthentication, ]
