from rest_framework import serializers

from quest.models import Quest, QuestType
from users.models import Employee, Student
from users.serializers import EmployeeSerializer, StudentSerializer


class QuestSerializer(serializers.ModelSerializer):
	employee_id = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
	student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), required=False)

	def to_representation(self, instance):
		representation = super().to_representation(instance)
		representation['employee'] = {
			'id': instance.employee_id.id,
			'first_name': instance.employee_id.first_name,
			'last_name': instance.employee_id.last_name,
			'user_role': instance.employee_id.user_role
		}
		student_id = instance.student_id
		if student_id:
			representation['student'] = {
				'id': student_id.id,
				'first_name': student_id.first_name,
				'last_name': student_id.last_name
			}
		else:
			representation['student'] = None
		representation.pop('employee_id')
		representation.pop('student_id')
		return representation

	class Meta:
		model = Quest
		fields = '__all__'


class QuestTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestType
		fields = '__all__'
