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


class StudentSerializer(BaseUserSerializer, GetStudentInfo):
	balance = serializers.SerializerMethodField()
	direction = DirectionSerializer(many=True, required=False)

	def create(self, validated_data):
		bank_account_id = BankAccount.objects.create(balance=int(os.environ.get('START_STUDENT_BALANCE')))
		hashed_password = make_password(validated_data.pop('password'))
		student_profile = StudentProfile.objects.create()
		student = Student.objects.create(
			bank_account_id=bank_account_id, student_profile=student_profile, **validated_data, password=hashed_password
		)
		return student

	def update(self, instance, validated_data):
		if 'password' in validated_data:
			validated_data['password'] = make_password(validated_data['password'])
		return super().update(instance, validated_data)

	class Meta:
		model = Student
		fields = BaseUserSerializer.Meta.fields + [
			'telegram', 'in_lite', 'status', 'portfolio_link', 'about', 'balance', 'image', 'direction'
		]
		extra_kwargs = {
			'image': {'required': False},
			'telegram': {'required': False},
			'portfolio_link': {'required': False},
			'about': {'required': False},
			'direction': {'required': False},
			'balance': {'required': False}
		}


class StudentUpdateSerializer(BaseUserSerializer, GetStudentInfo):
	class Meta:
		model = Student
		fields = BaseUserSerializer.Meta.fields + [
			'telegram', 'in_lite', 'status', 'portfolio_link', 'about', 'image', 'direction'
		]


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


class StudentProfileSerializer(
	serializers.ModelSerializer
):
	def get_student_id(self, obj):
		student_id = obj.student_id
		return StudentSerializer(student_id).data
	student_id = serializers.SerializerMethodField()

	class Meta:
		model = StudentProfile
		fields = '__all__'
