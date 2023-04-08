from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Student, Employee, CustomUser, BankAccount


class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    # class Meta:
    #     model = CustomUser
    #     fields = ['id', 'first_name', 'last_name', 'email', 'password']

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
        fields = '__all__'


class StudentSerializer(BaseUserSerializer):
    class Meta:  # (BaseUserSerializer.Meta):
        model = Student
        fields = '__all__'  # BaseUserSerializer.Meta.fields + ['telegram', 'in_lite', 'status', 'portfolio_link', 'about']


# class ShortStudentInfoSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Student
# 		fields = ['first_name', 'last_name', 'bank_account_id__balance']


class EmployeeSerializer(BaseUserSerializer):
    class Meta:
        model = Employee
        fields = '__all__'  # BaseUserSerializer.Meta.fields + ['employee_role', 'first_fact', 'second_fact', 'false_fact']
