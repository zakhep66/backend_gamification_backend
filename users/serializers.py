import os

from django.contrib.auth.hashers import make_password
from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Student, Employee, CustomUser, BankAccount, Direction, StudentProfile
from .users_relation_info_serializer import GetStudentInfo, BaseUserSerializer, GetEmployeeInfo


class BankAccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = BankAccount
		fields = ['id', 'balance', ]


class DirectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Direction
		fields = '__all__'


class ShortStudentInfoSerializer(serializers.ModelSerializer, GetStudentInfo):
	balance = serializers.SerializerMethodField()
	direction = DirectionSerializer(many=True)

	def get_student_profile(self, obj):
		student_profile = obj.student_profile
		return {
			'back_color': student_profile.back_color,
			'border_color': student_profile.border_color,
			'emoji_status': student_profile.emoji_status
		}

	student_profile = serializers.SerializerMethodField()

	class Meta:
		model = Student
		fields = ['id', 'first_name', 'last_name', 'balance', 'image', 'direction', 'student_profile']


class StudentProfileSerializer(
	serializers.ModelSerializer
):
	class Meta:
		model = StudentProfile
		fields = '__all__'


class StudentSerializer(BaseUserSerializer, GetStudentInfo):
	balance = serializers.SerializerMethodField()
	direction = serializers.PrimaryKeyRelatedField(queryset=Direction.objects.all(), many=True, required=False)
	student_profile = StudentProfileSerializer(required=False)

	def create(self, validated_data):
		direction_data = validated_data.pop('direction', [])
		bank_account_id = BankAccount.objects.create(balance=int(os.environ.get('START_STUDENT_BALANCE')))
		hashed_password = make_password(validated_data.pop('password'))
		student_profile = StudentProfile.objects.create()

		student = Student.objects.create(
			bank_account_id=bank_account_id,
			student_profile=student_profile,
			**validated_data,
			password=hashed_password
		)

		directions = Direction.objects.filter(id__in=direction_data)
		student.direction.set(directions)

		return student

	def update(self, instance, validated_data):
		if 'password' in validated_data:
			validated_data['password'] = make_password(validated_data['password'])

		student_profile_data = validated_data.pop('student_profile', None)

		if student_profile_data:
			student_profile = instance.student_profile
			for attr, value in student_profile_data.items():
				setattr(student_profile, attr, value)
			student_profile.save()

		if 'direction' in validated_data:
			direction_ids = validated_data.pop('direction')
			directions = Direction.objects.filter(id__in=direction_ids)
			instance.direction.set(directions)

		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		instance.save()

		return instance

	def to_internal_value(self, data):
		direction_data = data.pop('direction', [])
		student_profile_data = data.pop('student_profile', None)
		validated_data = super().to_internal_value(data)

		if student_profile_data:
			student_profile_serializer = StudentProfileSerializer(data=student_profile_data)
			student_profile_serializer.is_valid(raise_exception=True)
			validated_data['student_profile'] = student_profile_serializer.validated_data

		if direction_data:
			validated_data['direction'] = direction_data

		return validated_data

	def to_representation(self, instance):
		representation = super().to_representation(instance)
		representation['student_profile'] = StudentProfileSerializer(instance.student_profile).data
		representation['direction'] = DirectionSerializer(instance.direction.all(), many=True).data
		return representation

	class Meta:
		model = Student
		fields = BaseUserSerializer.Meta.fields + [
			'telegram', 'in_lite', 'status', 'portfolio_link', 'about', 'balance', 'image', 'direction',
			'student_profile'
		]
		extra_kwargs = {
			'image': {'required': False},
			'telegram': {'required': False},
			'portfolio_link': {'required': False},
			'about': {'required': False},
			'direction': {'required': False},
			'balance': {'required': False},
			'student_profile': {'required': False},
		}


# class StudentUpdateSerializer(BaseUserSerializer, GetStudentInfo):
# 	student_profile = StudentProfileSerializer()
#
# 	class Meta:
# 		model = Student
# 		fields = BaseUserSerializer.Meta.fields + [
# 			'telegram', 'in_lite', 'status', 'portfolio_link', 'about', 'image', 'direction', 'student_profile'
# 		]
#
# 	def update(self, instance, validated_data):
# 		profile_data = validated_data.pop('student_profile')
# 		student_profile = instance.student_profile
#
# 		# Обновление полей студента
# 		# for field, value in validated_data.items():
# 		# 	setattr(instance, field, value)
# 		# instance.save()
#
# 		# Обновление полей связанной модели
# 		for field, value in profile_data.items():
# 			setattr(student_profile, field, value)
# 		student_profile.save()


class EmployeeSerializer(BaseUserSerializer, GetEmployeeInfo):
	direction = serializers.SerializerMethodField()

	def create(self, validated_data):
		validated_data['password'] = make_password(validated_data['password'])
		return super().create(validated_data)

	def update(self, instance, validated_data):
		if 'password' in validated_data:
			validated_data['password'] = make_password(validated_data['password'])
		return super().update(instance, validated_data)

	class Meta:
		model = Employee
		fields = BaseUserSerializer.Meta.fields + [
			'first_fact', 'second_fact', 'false_fact', 'image', 'first_fact', 'second_fact', 'false_fact', 'direction'
		]
		extra_kwargs = {
			'image': {'required': False},
			'first_fact': {'required': False},
			'second_fact': {'required': False},
			'false_fact': {'required': False},
			'direction': {'required': False}
		}
