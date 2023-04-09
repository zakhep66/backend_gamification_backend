from rest_framework import viewsets, status
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Student, Employee, BankAccount
from .permissions import IsEmployee
from .serializers import StudentSerializer, EmployeeSerializer, BankAccountSerializer, \
    ShortStudentInfoSerializer  # , ShortStudentInfoSerializer


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
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [CustomAuthentication, ]

    def get_permissions(self):
        """
        Определяем права доступа к методам.
        """

        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, ]
        elif self.action in ['create', 'partial_update', 'update']:
            permission_classes = [IsEmployee, ]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        bank_account_data = request.data.get('bank_account')
        if bank_account_data:
            bank_account_serializer = BankAccountSerializer(data=bank_account_data)
            if bank_account_serializer.is_valid():
                bank_account = bank_account_serializer.save()
                request.data['bank_account_id'] = bank_account.id
            else:
                return Response(bank_account_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


class ShortStudentInfoViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = ShortStudentInfoSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [CustomAuthentication, ]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


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

            data = {
                'email': employee.email,
                'user_role': employee.user_role,
                'first_name': employee.first_name,
                'last_name': employee.last_name,
            }

            if employee.image:
                data['image'] = employee.image.url
            if employee.first_fact:
                data['first_fact'] = employee.first_fact
            if employee.second_fact:
                data['second_fact'] = employee.second_fact
            if employee.false_fact:
                data['false_fact'] = employee.false_fact

            return Response(data)

        except Employee.DoesNotExist:
            pass

        try:
            student = Student.objects.get(id=user_id)
            # профиль студента

            data = {
                'email': student.email,
                'user_role': student.user_role,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'balance': student.bank_account_id.balance,
                'about': student.about
            }

            if student.image:
                data['image'] = student.image.url
            if student.telegram:
                data['telegram'] = student.telegram
            if student.about:
                data['about'] = student.about
            if student.portfolio_link:
                data['portfolio_link'] = student.portfolio_link
            if student.direction.all().exists():
                data['directions'] = [
                    {'name': direction.name, 'link': direction.icon}
                    for direction in student.direction.all()
                ]

            return Response(data)

        except Student.DoesNotExist:
            pass

        return Response({'error': 'Пользователь не найден.'}, status=404)

