from rest_framework import viewsets
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Student, Employee
from .permissions import IsEmployee
from .serializers import StudentSerializer, EmployeeSerializer


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = JWTAuthentication()

        # Получаем пользователя и токен из запроса
        user, token = auth.authenticate(request)

        # Возвращаем кортеж (пользователь, токен)
        return user, token


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра и редактирования пользователей.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsEmployee, IsAdminUser, ]
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


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра и редактирования пользователей.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [CustomAuthentication, ]


class ProfileView(APIView):
    authentication_classes = [CustomAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user_id = request.user.id
        try:
            employee = Employee.objects.get(id=user_id)
            # профиль сотрудника
            return Response(
                {
                    'email': employee.email,
                    'employee_role': employee.employee_role,
                    'first_name': employee.first_name,
                    'last_name': employee.last_name,
                    'image': employee.image.url,
                    'first_fact': employee.first_fact,
                    'second_fact': employee.second_fact,
                    'false_fact': employee.false_fact
                }
            )
        except Employee.DoesNotExist:
            pass

        try:
            student = Student.objects.get(id=user_id)
            # профиль студента
            return Response(
                {
                    'email': student.email,
                    'first_name': student.first_name,
                    'last_name': student.last_name,
                    'image': student.image.url,
                    'telegram': student.telegram,
                    'balance': student.bank_account_id.balance,
                    'portfolio_link': student.portfolio_link,
                    'directions': [
                        {'name': direction.name, 'link': direction.icon}
                        for direction in student.direction.all()
                    ],
                    'about': student.about
                }
            )
        except Student.DoesNotExist:
            pass

        return Response({'error': 'Пользователь не найден.'}, status=404)
