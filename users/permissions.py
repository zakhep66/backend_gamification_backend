from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions

from .models import Employee


class IsEmployee(permissions.BasePermission):
    """
     Разрешает доступ только пользователям, которые являются экземплярами модели Employee.
     """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                return isinstance(request.user.employee, Employee)
            except ObjectDoesNotExist:
                return False
        return False
