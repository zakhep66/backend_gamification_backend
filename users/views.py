from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import CustomUser
from .serializers import StudentSerializer, EmployeeSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра и редактирования пользователей.
    """
    queryset = CustomUser.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра и редактирования пользователей.
    """
    queryset = CustomUser.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
