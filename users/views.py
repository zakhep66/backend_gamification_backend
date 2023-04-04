from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, BaseAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from .models import Student, Employee
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
    permission_classes = [IsAdminUser, ]
    authentication_classes = [CustomAuthentication, ]


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра и редактирования пользователей.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminUser, ]
    authentication_classes = [CustomAuthentication, ]


class ProfileView(APIView):
    authentication_classes = [CustomAuthentication, ]

    def get(self, request):
        # Получаем модель пользователя из аутентификационного класса
        user_model = request.user.__class__

        # Сериализуем данные пользователя в зависимости от его модели
        if user_model.is_staff is False:
            serializer = StudentSerializer(instance=request.user)
        elif user_model.is_staff:
            serializer = EmployeeSerializer(instance=request.user)
        else:
            return Response({'detail': 'Invalid user type in token'})

        return Response(serializer.data)
