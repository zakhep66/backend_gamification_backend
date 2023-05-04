import os

from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, OR
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from .models import Student, Employee, BankAccount, StudentProfile
from .permissions import IsEmployeeManager, IsEmployeeManagerOrCouch
from .serializers import StudentSerializer, EmployeeSerializer, BankAccountSerializer, \
    ShortStudentInfoSerializer, StudentProfileSerializer


class CustomAuthentication(BaseAuthentication):
    def check_token(self, request):
        auth = JWTAuthentication()
        return auth.authenticate(request)

    def authenticate(self, request):
        user_token = self.check_token(request)
        if user_token is not None:
            user, token = user_token
            # дополнительная логика проверки пользовательских прав и разрешений здесь, если это необходимо
            return user, token
        else:
            return None


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра и редактирования пользователей.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [CustomAuthentication, ]

    def get_permissions(self):
        """
        Определяем права доступа к методам.
        """

        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, ]
        elif self.action in ['create', 'partial_update', 'update']:
            permission_classes = [IsEmployeeManagerOrCouch, ]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = StudentSerializer(instance)
        return Response(serializer.data)


class ShortStudentInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = ShortStudentInfoSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [CustomAuthentication, ]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = StudentSerializer(instance)
        return Response(serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра и редактирования пользователей.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminUser | IsEmployeeManager, ]
    authentication_classes = [CustomAuthentication, ]

    def get_permissions(self):
        """
        Определяем права доступа к методам.
        """

        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = EmployeeSerializer(instance)
        return Response(serializer.data)


class ProfileView(APIView):
    authentication_classes = [CustomAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user_id = request.user.id
        try:
            employee = Employee.objects.get(id=user_id)
            # профиль сотрудника

            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)

        except Employee.DoesNotExist:
            pass

        try:
            student = Student.objects.get(id=user_id)
            # профиль студента
            serializer = StudentSerializer(student)
            return Response(serializer.data)

        except Student.DoesNotExist:
            pass

        return Response({'error': 'Пользователь не найден.'}, status=404)

    def patch(self, request):
        user_id = request.user.id

        try:
            employee = Employee.objects.get(id=user_id)
            # обновление профиля сотрудника

            serializer = EmployeeSerializer(instance=employee, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)

        except Employee.DoesNotExist:
            pass

        try:
            student = Student.objects.get(id=user_id)

            if 'password' in request.data:
                request.data.pop('password')

            serializer = StudentSerializer(instance=student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)

        except Student.DoesNotExist:
            pass

        return Response({'error': 'Пользователь не найден.'}, status=404)
