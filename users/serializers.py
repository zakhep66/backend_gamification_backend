from rest_framework import serializers
from .models import Student, Employee, CustomUser


class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'password']

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


class StudentSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = Student
        fields = BaseUserSerializer.Meta.fields + ['telegram', 'in_lite', 'status', 'portfolio_link', 'about']


class EmployeeSerializer(BaseUserSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    employee_role = serializers.CharField(source='user.employee_role', read_only=True)

    class Meta:
        model = Employee
        fields = BaseUserSerializer.Meta.fields + ['employee_role', 'first_fact', 'second_fact', 'false_fact']
