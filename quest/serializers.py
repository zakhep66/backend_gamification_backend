from rest_framework import serializers

from quest.models import Quest, QuestType
from users.serializers import EmployeeSerializer, StudentSerializer


class QuestSerializer(serializers.ModelSerializer):
	employee_id = serializers.SerializerMethodField()
	student_id = serializers.SerializerMethodField()

	def get_employee_id(self, obj):
		return {
			'id': obj.employee_id.id,
			'first_name': obj.employee_id.first_name,
			'last_name': obj.employee_id.last_name,
			'user_role': obj.employee_id.user_role
		}

	def get_student_id(self, obj):
		return {
			'id': obj.student_id.id,
			'first_name': obj.student_id.first_name,
			'last_name': obj.student_id.last_name
		} if obj.student_id else None

	class Meta:
		model = Quest
		fields = '__all__'


class QuestTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestType
		fields = '__all__'
