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


class IsEmployeeManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                employee = request.user.employee
                if employee.user_role == 'manager':
                    return True
            except ObjectDoesNotExist:
                pass
        return False


class MakeCreateStudentsUpdates(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                employee = request.user.employee
                if employee.user_role in ['manager', 'couch']:
                    return True
            except ObjectDoesNotExist:
                pass
            return False
