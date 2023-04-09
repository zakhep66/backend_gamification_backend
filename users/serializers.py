from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Student, Employee, CustomUser, BankAccount, Direction


class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = ...
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'user_role']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['id', 'balance', ]


class GetStudentBalance:
    def get_balance(self, obj):
        bank_account = obj.bank_account_id
        return bank_account.balance if bank_account else None


class StudentSerializer(BaseUserSerializer, GetStudentBalance):
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = BaseUserSerializer.Meta.fields + ['telegram', 'in_lite', 'status', 'portfolio_link', 'about',
                                                   'balance', 'image', ]


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ['name', 'icon']


class ShortStudentInfoSerializer(serializers.ModelSerializer, GetStudentBalance):
    balance = serializers.SerializerMethodField()
    direction = DirectionSerializer(many=True)

    def get_direction(self, obj):
        direction = obj.direction
        return DirectionSerializer(direction, many=True).data

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'balance', 'image', 'direction']


class EmployeeSerializer(BaseUserSerializer):
    class Meta:
        model = Employee
        fields = BaseUserSerializer.Meta.fields + ['first_fact', 'second_fact', 'false_fact']
